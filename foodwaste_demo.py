
import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import holidays

import plotly.express as px
import plotly.graph_objects as go

from foodwaste_demo_ai import * 
from foodwaste_demo_strings import * 
from foodwaste_demo_syntheticdata import * 

# options
# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

if "language" not in st.session_state:
    st.session_state.language = "Deutsch"
# more on language in foodwaste_demo_strings.py

if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "show_info" not in st.session_state:
    st.session_state.show_info = False

if "budget" not in st.session_state:
    st.session_state.budget = 2000  # starting budget

# AI preparations
# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

if "ai_model" not in st.session_state:
    st.session_state.ai_model = get_localized_string("modelHeu", st.session_state.language)
if "order_prediction" not in st.session_state:
    st.session_state.order_prediction = 0
if "prediction_explanation" not in st.session_state:
    st.session_state.prediction_explanation = None
if "show_ai_explanation" not in st.session_state:
    st.session_state.show_ai_explanation = False

# more in foodwaste_demo_ai.py

# begin streamlit page
# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

st.set_page_config(page_title="KI-Kuchenbestellung", layout="centered")

# historical data 
# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

# On starting the interface, generate a synthetic data history
if "data" not in st.session_state:
    k = 3 
    start_date = datetime.today() - timedelta(days=k*365)  # k years ago
    end_date = datetime.today() # Up to, including today (today's ordering was yesterday)
    #end_date = datetime.today() - timedelta(days=7) # Debugging Aid
    st.session_state.data = generate_synthetic_data(start_date, end_date, st.session_state.language)

# And create a current tomorrow
if "tomorrow_info" not in st.session_state:
    st.session_state.tomorrow_info = generate_tomorrow(st.session_state.data, st.session_state.language)

# more in foodwaste_demo_syntheticdata.py

# streamlit page 
# ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- ------- ---- -------

# --- SIDEBAR CONTROLS ---

#st.sidebar.write("## ⚙️ " + get_localized_string("options", st.session_state.language))
st.sidebar.write("## ⚙️")
st.session_state.language = st.sidebar.radio("Sprache / Language", ["Deutsch", "English"])
st.session_state.show_history = st.sidebar.toggle(get_localized_string("showhistory", st.session_state.language), value=st.session_state.show_history)
st.session_state.show_info = st.sidebar.toggle(get_localized_string("showinfo", st.session_state.language), value=st.session_state.show_info)

# Budget Tracking 
st.sidebar.write("---")
st.sidebar.metric("Budget", f"€{st.session_state.budget:,.2f}")
st.sidebar.write(get_localized_string("budgetExplanation", st.session_state.language))

# Oh, and show the logo
# st.sidebar.write("")
# st.sidebar.write("")
# st.sidebar.write("")
# st.sidebar.write("----")
# st.sidebar.write("")
# st.sidebar.image("logo_digital_black.png", width=100)

# --- TITLE AND INTRO ---

st.title(get_localized_string("heading1", st.session_state.language))
st.write(get_localized_string("introtext", st.session_state.language))

# --- INFO TEXT ---

if st.session_state.show_info:
    st.info(get_localized_string("infotext", st.session_state.language))

# --- HISTORICAL DATA VIEW ---

if st.session_state.show_history:
    st.subheader(get_localized_string("salesHistory", st.session_state.language))

    # Show latest table entries
    #st.write(st.session_state.data.tail())
    #st.write(st.session_state.data) # or all entries
    
    # Filter last 14 days by default
    full_data = st.session_state.data  # All historical data
    last_two_weeks_start = st.session_state.data["date"].iloc[-1] - timedelta(days=14)
    mondays = full_data["date"][full_data["date"].dt.weekday == 0]
    
    # plot view with tabs 
    sales_tab, weather_tab = st.tabs([
        get_localized_string("salesHistory", st.session_state.language),
        get_localized_string("weatherHistory", st.session_state.language)
    ])

    with sales_tab:
        # sales plot
        fig_sales = px.line(
            full_data,
            x="date",
            y=["sales", "order"],
            labels={
                "date": get_localized_string("dateAxis", st.session_state.language),
                "sales": get_localized_string("salesAxis", st.session_state.language),
                "order": get_localized_string("orderAxis", st.session_state.language),
            },
            title=get_localized_string("salesHistory", st.session_state.language),
        )
        # week separators 
        fig_sales.update_layout(
            shapes=[
                dict(
                    type="line",
                    x0=monday,
                    x1=monday,
                    y0=full_data["sales"].min(),
                    y1=full_data["sales"].max(),
                    line=dict(color="lightgrey", width=1, dash="dot"),
                )
                for monday in mondays
            ],
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date",
                range=[last_two_weeks_start, st.session_state.data["date"].iloc[-1]],
            ),
            yaxis=dict(fixedrange=True),
        )
        # show chart
        st.plotly_chart(fig_sales, use_container_width=True)

    with weather_tab:
        # weather plot
        fig_temp = px.line(
            full_data,
            x="date",
            y="temperature",
            labels={
                "date": get_localized_string("dateAxis", st.session_state.language),
                "temperature": get_localized_string("temperatureAxis", st.session_state.language),
            },
            title=get_localized_string("weatherHistory", st.session_state.language),
        )
        # week separators
        fig_temp.update_layout(
            shapes=[
                dict(
                    type="line",
                    x0=monday,
                    x1=monday,
                    y0=full_data["temperature"].min(),
                    y1=full_data["temperature"].max(),
                    line=dict(color="lightgrey", width=1, dash="dot"),
                )
                for monday in mondays
            ],
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date",
                range=[last_two_weeks_start, st.session_state.data["date"].iloc[-1]],
            ),
            yaxis=dict(fixedrange=True),
        )
        # add weather icons 
        weather_subset = full_data
        fig_temp.add_trace(
            go.Scatter(
                x=weather_subset["date"],
                y=[full_data["temperature"].min()] * len(weather_subset), # all at 0°C
                text=weather_subset["weather"],
                mode="text", 
                textposition="top center",
                textfont=dict(size=16), # icon size
                name=get_localized_string("weatherAxis", st.session_state.language)
            )
        )
        # show chart
        st.plotly_chart(fig_temp, use_container_width=True)


# --- ORDERING TILE ---

rerun_later = False 

ordering_tile = st.container(border=True)
with ordering_tile:
    st.subheader(get_localized_string("orderingtitle", st.session_state.language))
day_info_col, ordering_col, ai_col = ordering_tile.columns([1, 1, 1], vertical_alignment="top")

with day_info_col:
    st.write(f"{get_localized_string("tomorrow", st.session_state.language)} **{get_localized_string(st.session_state.tomorrow_info.get("dayofweek"), st.session_state.language)}, {st.session_state.tomorrow_info.get("date").strftime('%d.%m.%Y')}**")
    if st.session_state.tomorrow_info.get("daytype") != "normal" and "before" not in st.session_state.tomorrow_info.get("daytype") and "after" not in st.session_state.tomorrow_info.get("daytype"):
        day_overview_string = "- " + get_localized_string("holidayevent", st.session_state.language)
    else: 
        day_overview_string = f"- {get_localized_string("weather", st.session_state.language)}: {st.session_state.tomorrow_info.get("weather")}" + "\n" + \
            f"- {get_localized_string("temperature", st.session_state.language)}: {st.session_state.tomorrow_info.get("temperature")}°C" + "\n" + \
            f"- {get_localized_string("daytype", st.session_state.language)}: {st.session_state.tomorrow_info.get("daytype")}"
    st.write(day_overview_string)

with ordering_col:

    ordered_cakes = st.number_input(get_localized_string("ordercommand", st.session_state.language), min_value=0, value=st.session_state.order_prediction, step=1)

    if st.button(get_localized_string("endday", st.session_state.language)):

        actual_sales = st.session_state.tomorrow_info["sales"]
        leftover = max(ordered_cakes - actual_sales, 0)
        missed = max(actual_sales - ordered_cakes, 0)
        unexpected_event = st.session_state.tomorrow_info["unexpected"]

        # End current day and update history
        current_day = st.session_state.tomorrow_info
        current_day["order"] = ordered_cakes
        current_day["leftover"] = leftover
        current_day["missed"] = missed
        new_row = pd.DataFrame(current_day, index=[st.session_state.data.index[-1] + 1])
        st.session_state.data = pd.concat([st.session_state.data, new_row])

        # Update Budget according to order 
        cost_of_order = ordered_cakes * 2  # €2 per cake
        cakes_sold = ordered_cakes - leftover
        revenue_from_sales = cakes_sold * 3  # €3 per cake
        st.session_state.budget += revenue_from_sales - cost_of_order

        # Generate a new tomorrow
        st.session_state.tomorrow_info = generate_tomorrow(st.session_state.data, st.session_state.language)
        st.session_state.summary = (actual_sales, leftover, missed, unexpected_event)

        # And update the interface (below) to show effects
        st.session_state.order_prediction = 0 # reset prediction
        st.session_state.prediction_explanation =  None # reset explanation
        rerun_later = True 

with ai_col:

    if st.button("<- " + get_localized_string("aiHelp", st.session_state.language)):
        predicted_order, prediction_explanation = predict_tomorrow_sales_with(st.session_state.data, st.session_state.tomorrow_info, st.session_state.ai_model, st.session_state.language)
        st.session_state.order_prediction = int(predicted_order) # Store prediction as int
        st.session_state.prediction_explanation = prediction_explanation # Store explanation
        rerun_later = True

    st.session_state.ai_model = st.selectbox(
        label=get_localized_string("modelLabel", st.session_state.language),
        options=[
            get_localized_string("modelHeu", st.session_state.language),
            get_localized_string("modelKNN", st.session_state.language),
            get_localized_string("modelXGB", st.session_state.language),
        ],
    )

    st.session_state.show_ai_explanation = st.toggle(get_localized_string("explainButton", st.session_state.language), value=st.session_state.show_ai_explanation)


# --- SHOW AI EXPLANATION IF AVAILABLE ---

if st.session_state.show_ai_explanation:
    explanation_tile = st.container(border=True)
    with explanation_tile:
        st.subheader(get_localized_string("modelExplanation", st.session_state.language))
        if st.session_state.prediction_explanation:
            # show basic model explanation
            st.write(get_localized_string(st.session_state.prediction_explanation.get("model_info"), st.session_state.language))
            # show reference days, if available 
            ref_days = st.session_state.prediction_explanation.get("reference_days")
            if ref_days:
                ref_day_cols = explanation_tile.columns([1 for ref_day in ref_days], vertical_alignment="top")
                for idx, col in enumerate(ref_day_cols):
                    with col:
                        st.write(f"- {str(ref_days[idx].get("date"))[:10]}" + "\n" + \
                            f"- {get_localized_string(ref_days[idx].get("dayofweek"), st.session_state.language)}" + "\n" + \
                            f"- {get_localized_string("sales", st.session_state.language)}: {ref_days[idx].get("sales")}" + "\n" + \
                            f"- {get_localized_string("weather", st.session_state.language)}: {ref_days[idx].get("weather")}" + "\n" + \
                            f"- {get_localized_string("temperature", st.session_state.language)}: {ref_days[idx].get("temperature")} °C" + "\n" + \
                            f"- {get_localized_string("daytype", st.session_state.language)}: {ref_days[idx].get("daytype")}"# + "\n" + \
                            #((f"- {get_localized_string("unexpectedevent", st.session_state.language)} - {ref_days[idx].get("unexpected")}") if ref_days[idx].get("unexpected") != "" else "")
                        )
        else: 
            st.write(get_localized_string("noModelExplanationAvailable", st.session_state.language))

# later is now
if rerun_later:
    st.rerun()

# --- RESULT SUMMARY TILE ---

if "summary" in st.session_state:

    actual_sales, leftover, missed, unexpected_event = st.session_state.summary

    summary_tile = st.container(border=True)
    with summary_tile:
        st.subheader(get_localized_string("resultsummary", st.session_state.language))
    result_col, feedback_col = summary_tile.columns([1, 1], vertical_alignment="center")

    with result_col:
        # TODO maybe turn into a table for better viewing
        result_string = f"- {get_localized_string("orderAxis", st.session_state.language)}: {st.session_state.data["order"].values[-1]}" + "\n" + \
            f"- {get_localized_string("resultsold", st.session_state.language)}: {actual_sales}" + "\n" + \
            f"- {get_localized_string("resultleftover", st.session_state.language)}: {leftover}" + "\n" + \
            f"- {get_localized_string("resultmissed", st.session_state.language)}: {missed}" + \
            (("\n" + f"- ⚠️ {get_localized_string("unexpectedevent", st.session_state.language)} - {unexpected_event}") if unexpected_event != "" else "")
        st.write(result_string)
        
    with feedback_col:
        if leftover > actual_sales/10: # 10% miss
            st.error(get_localized_string("feedbackTooMany", st.session_state.language))
        elif leftover > actual_sales/20: # 5% miss
            st.warning(get_localized_string("feedbackTooMany", st.session_state.language))
        elif missed > actual_sales/10: # 10% miss
            st.error(get_localized_string("feedbackTooFew", st.session_state.language))
        elif missed > actual_sales/20: # 5% miss
            st.warning(get_localized_string("feedbackTooFew", st.session_state.language))
        else:
            st.success(get_localized_string("feedbackJustRight", st.session_state.language))

