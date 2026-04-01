import streamlit as st
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import pandas as pd
import textwrap
import re

st.set_page_config(
    page_title="Advanced Poisson Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #1e293b;
    }
    .stats-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stats-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .stats-card h3 {
        margin: 0;
        font-size: 1.05rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
    }
    .stats-card h2 {
        margin: 12px 0 0 0;
        font-size: 2.5rem;
        color: #0ea5e9;
        font-weight: 800;
    }
    .interpretation-card {
        background-color: #f0fdf4;
        border-left: 6px solid #22c55e;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .interpretation-card p, .interpretation-card li {
        color: #166534;
        font-size: 1.1rem;
    }
    .theory-section {
        background-color: white;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Adding futuristic animations and sleek design enhancements
st.markdown("""
<style>
    /* Futuristic Background Animation */
    body {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e2e8f0;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Button Hover Animation */
    .stButton button {
        background: linear-gradient(90deg, #0ea5e9, #3b82f6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #3b82f6, #0ea5e9);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
    }

    /* Card Glow Effect */
    .stats-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stats-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.4);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(90deg, #0ea5e9, #3b82f6);
        color: white;
        border-radius: 8px;
        margin: 0 0.5rem;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(90deg, #3b82f6, #0ea5e9);
        transform: scale(1.05);
    }

    /* Header Animation */
    h1, h2, h3 {
        animation: fadeIn 2s ease;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Application Title
st.title("📊 Advanced Poisson Distribution Learning Hub")
st.markdown("<p style='font-size: 1.1rem; color: #475569;'>Enter your inputs dynamically to simulate probabilities and explore the underlying mathematical theory.</p>", unsafe_allow_html=True)

# Create two primary tabs
tab_sim, tab_info = st.tabs(["🎮 Interactive Simulator", "📚 Poisson Distribution Info (Theory)"])

# ----------------------------------------
# 1. SIMULATOR TAB
# ----------------------------------------

    
    question = st.sidebar.text_area(
        "Real-World Question / Context (Optional)", 
        placeholder="e.g., A call center processes calls with a 0.05 probability per customer out of 200 customers...",
        help="Entering a question helps the Smart Interpretation explicitly explain your scenario.",
        key="question_input",
        height=150
    )
    
    st.sidebar.button("Solve", on_click=parse_question, help="Automatically extract n and p from your question.")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Mathematical Model Inputs")
    st.sidebar.markdown("The Poisson limit requires $n$ and $p$. Lambda (λ) is computed strictly as $n \\times p$.")

    # Dynamic Inputs tied to session state
    n = st.sidebar.number_input("Number of Trials (n)", min_value=1, max_value=1000000, key="n_val", step=10)
    p = st.sidebar.number_input("Probability of Success (p)", min_value=0.0001, max_value=0.9999, key="p_val", step=0.001, format="%.4f")
    
    # Core Math Calculation
    lam = n * p
    
    st.sidebar.markdown(f"""
    <div style='background-color: #e0f2fe; padding: 1rem; border-radius: 8px; border: 1px solid #bae6fd; margin-top: 1rem; text-align: center;'>
        <h4 style='color: #0369a1; margin: 0;'>Calculated Lambda (λ)</h4>
        <h2 style='color: #0284c7; margin: 0; font-size: 2.5rem;'>{lam:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    viz_mode = st.sidebar.radio("Visualization Dashboard Mode", ["2D Interactive View (Plotly)", "3D Bar View (Required)"])

    # Simulator calculations limits
    max_k = int(max(lam * 3, 10))
    k = np.arange(0, max_k + 1)
    
    pmf = stats.poisson.pmf(k, lam)
    samples = np.random.poisson(lam, n)  # Using n trials for the sample generation
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
        <div class="stats-card">
            <h3>Theoretical Mean (μ = λ)</h3>
            <h2>{lam:.2f}</h2>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="stats-card">
            <h3>Theoretical Var (σ² = λ)</h3>
            <h2>{lam:.2f}</h2>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="stats-card">
            <h3>Simulation Sample Mean</h3>
            <h2>{np.mean(samples):.2f}</h2>
        </div>
        ''', unsafe_allow_html=True)

    # Visualization Layer
    st.header("📈 Visualizations", divider="blue")
    
    if viz_mode == "2D Interactive View (Plotly)":
        col_plot1, col_plot2 = st.columns(2)
        with col_plot1:
            st.subheader("Poisson PMF (Theory)")
            fig_pmf = go.Figure()
            fig_pmf.add_trace(go.Bar(
                x=k, y=pmf, name=f'λ={lam:.2f}', marker_color='#0ea5e9',
                hovertemplate="Events (k): %{x}<br>Probability: %{y:.4f}<extra></extra>"
            ))
            fig_pmf.update_layout(xaxis_title="Number of Successes (k)", yaxis_title="Probability (PMF)",
                                  margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='rgba(0,0,0,0)', hovermode="x unified")
            st.plotly_chart(fig_pmf, use_container_width=True)

        with col_plot2:
            st.subheader(f"Simulated Data Histogram (n={n})")
            counts, bins = np.histogram(samples, bins=np.arange(0, max(samples)+2))
            probs = counts / n
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Bar(
                x=bins[:-1], y=probs, name=f'Simulated (λ≈{np.mean(samples):.2f})', marker_color='#10b981',
                hovertemplate="Events (k): %{x}<br>Relative Frequency: %{y:.4f}<extra></extra>"
            ))
            fig_hist.update_layout(xaxis_title="Number of Successes (k)", yaxis_title="Relative Frequency",
                                  margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='rgba(0,0,0,0)', hovermode="x unified")
            st.plotly_chart(fig_hist, use_container_width=True)
            
    else:
        # Constraint: Matplotlib 3D Charts
        col_plot1, col_plot2 = st.columns(2)
        
        with col_plot1:
            st.subheader("Poisson PMF (Theoretical 3D)")
            fig_pmf = plt.figure(figsize=(7, 6))
            ax = fig_pmf.add_subplot(111, projection='3d')
            y = np.ones_like(k)
            z = np.zeros_like(k)
            dx = np.ones_like(k) * 0.5
            dy = np.ones_like(k) * 0.5
            colors = plt.cm.Blues(0.4 + 0.6*(pmf / max(pmf)))
            ax.bar3d(k - 0.25, y, z, dx, dy, pmf, color=colors, shade=True, alpha=0.9)
            ax.set_yticks([])
            ax.set_xlabel('Successes (k)')
            ax.set_zlabel('Probability')
            ax.view_init(elev=20, azim=-50)
            st.pyplot(fig_pmf)

        with col_plot2:
            st.subheader(f"Simulated Histogram 3D (n={n})")
            fig_hist = plt.figure(figsize=(7, 6))
            ax2 = fig_hist.add_subplot(111, projection='3d')
            counts, bins = np.histogram(samples, bins=np.arange(0, max(samples)+2))
            probs = counts / n
            x_pos = bins[:-1]
            y_pos = np.ones_like(x_pos)
            z_pos = np.zeros_like(x_pos)
            dx_pos = np.ones_like(x_pos) * 0.5
            dy_pos = np.ones_like(x_pos) * 0.5
            colors_hist = plt.cm.Greens(0.4 + 0.6*(probs / (max(probs) if max(probs)>0 else 1)))
            ax2.bar3d(x_pos - 0.25, y_pos, z_pos, dx_pos, dy_pos, probs, color=colors_hist, shade=True, alpha=0.9)
            ax2.set_yticks([])
            ax2.set_xlabel('Successes (k)')
            ax2.set_zlabel('Relative Frequency')
            ax2.view_init(elev=20, azim=-50)
            st.pyplot(fig_hist)


    # Cumulative Probability Calculator
    st.header("🧮 Cumulative Probability Calculator", divider="blue")
    
    col_calc1, col_calc2, col_calc3 = st.columns([1, 1.5, 1.5])
    
    with col_calc1:
        calc_k = st.number_input("Number of Events (k)", min_value=0, max_value=max_k*5, value=int(lam) if int(lam) <= max_k*5 else 0, step=1)
        
    with col_calc2:
        calc_type = st.selectbox("Probability Type", [
            "P(X = k) → Exact probability",
            "P(X ≤ k) → At most k events",
            "P(X ≥ k) → At least k events"
        ])
        
    with col_calc3:
        if "X = k" in calc_type:
            prob_res = stats.poisson.pmf(calc_k, lam)
            exp_text = f"This is the probability of exactly {calc_k} events occurring."
        elif "X ≤ k" in calc_type:
            prob_res = stats.poisson.cdf(calc_k, lam)
            exp_text = f"This represents the probability of at most {calc_k} events."
        else:
            if calc_k == 0:
                prob_res = 1.0
            else:
                prob_res = 1.0 - stats.poisson.cdf(calc_k - 1, lam)
            exp_text = f"This represents the probability of {calc_k} or more events."
            
        st.markdown(f"""
        <div style='background-color: #f8fafc; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; margin-bottom: 0.5rem;'>
            <h4 style='color: #64748b; margin: 0; font-size: 0.9rem; text-transform: uppercase;'>Calculated Probability</h4>
            <h2 style='color: #0ea5e9; margin: 5px 0 0 0; font-size: 2rem;'>{prob_res:.4f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    st.info(f"💡 **Explanation:** {exp_text}")
    st.markdown("<br>", unsafe_allow_html=True)

    # Smart Interpretation Section
    st.header("🧠 Smart Interpretation", divider="blue")
    
    peak_val = int(lam)
    
    interpretation_html = f"""
<div class="interpretation-card">
<h3 style="margin-top: 0; color: #15803d;">📝 Contextual Analysis</h3>
<p><b>Your Input Scenario:</b> <i>"{question if question.strip() else 'No explicit contextual scenario was provided in the sidebar.'}"</i></p>

<hr style="border: 1px solid #bbf7d0; margin: 15px 0;">

<h4>1. Understanding Lambda in Your Context</h4>
<ul>
<li>By providing <b>{n} trials</b> and a probability of <b>{p:.4f}</b> per trial, the system computed the expected average occurrence rate (<b>λ</b>) as exactly <b>{lam:.2f}</b>.</li>
<li>This means that on average, in your specific scenario, you can expect exactly <b>{lam:.2f}</b> successes (or events) to occur.</li>
</ul>

<h4>2. Graph Behavior & Probability Distribution</h4>
<ul>
<li>The shape of the probability graph peaks around <b>k = {peak_val}</b>. This graphically validates that testing exactly {peak_val} successful events is the single most likely outcome.</li>
<li>Because the Variance is dynamically bound tightly to the Mean (Variance = {lam:.2f}), {np.sum(pmf[max(0, int(lam - np.sqrt(lam))):int(lam + np.sqrt(lam))]*100):.1f}% of your data statistically bundles immediately surrounding the mean {lam:.2f}.</li>
</ul>

<h4>3. Simulation vs. Theory</h4>
<ul>
<li>We simulated evaluating {n} active trials relying heavily on Poisson behavior.</li>
<li>The empirical simulated mean successfully matched to <b>{np.mean(samples):.2f}</b>, mirroring the theoretical Mean (<b>{lam:.2f}</b>), proving the <i>Law of Large Numbers</i> effectively governs this distribution.</li>
</ul>
</div>
    """
    st.markdown(interpretation_html, unsafe_allow_html=True)

# ----------------------------------------
# 2. INFORMATION TAB (THEORY)
# ----------------------------------------
with tab_info:
    st.markdown("""
<div class="theory-section">
<h1 style="color: #0ea5e9; font-size: 2.2rem; margin-bottom: 2rem;">Theoretical Framework: The Poisson Distribution</h1>

<h3 style="color: #334155;">1. Definition</h3>
<p style="font-size: 1.1rem; line-height: 1.6; color: #475569;">
The Poisson distribution is a discrete probability distribution that expresses the probability of a given number of events occurring in a fixed interval of time or space if these events occur with a known constant mean rate and independently of the time since the last event.
</p>

<hr style="border-top: 1px dashed #cbd5e1; margin: 2rem 0;">

<h3 style="color: #334155;">2. Core Mathematical Formula</h3>
<div style="background-color: #f8fafc; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; margin: 1.5rem 0;">
<p style="font-size: 1.5rem; font-family: monospace; color: #0284c7; margin: 0;">
P(X = k) = (λ<sup>k</sup> * e<sup>-λ</sup>) / k!
</p>
</div>

<h4 style="color: #334155;">Explanation of Terms:</h4>
<ul style="font-size: 1.1rem; color: #475569; line-height: 1.8;">
<li><b>P(X = k):</b> The calculated probability of observing exactly <b>k</b> successful events in the interval.</li>
<li><b>λ (Lambda):</b> The average number of events in an interval. It represents both the Expected Value and the Variance.</li>
<li><b>k (Successful Events):</b> The number of occurrences of an event — the probability of which is given by the function.</li>
<li><b>e:</b> Euler's number (approximately 2.71828), which is the base of the natural logarithm.</li>
<li><b>k!:</b> The factorial of k.</li>
</ul>

<hr style="border-top: 1px dashed #cbd5e1; margin: 2rem 0;">

<h3 style="color: #334155;">3. Relation with Binomial Distribution (λ = n × p)</h3>
<p style="font-size: 1.1rem; line-height: 1.6; color: #475569;">
The Poisson distribution is deeply interconnected with the Binomial Distribution. It is inherently derived as the limit of the binomial distribution where the number of trials (<b>n</b>) approaches infinity, and the probability of success (<b>p</b>) approaches zero, but the product <b>n × p</b> remains a constant exactly equating to the average expected events. In mathematical terms:<br><br>
<strong>λ = n × p</strong>
</p>

<hr style="border-top: 1px dashed #cbd5e1; margin: 2rem 0;">

<div style="display: flex; gap: 2rem;">
<div style="flex: 1;">
<h3 style="color: #334155;">4. Crucial Properties</h3>
<ul style="font-size: 1.1rem; color: #475569; line-height: 1.8;">
<li><strong>Mean (μ):</strong> Exactly equates to λ.</li>
<li><strong>Variance (σ²):</strong> Exactly equates to λ. This implies the standard deviation expands precisely via the square root of λ.</li>
<li><strong>Skewness:</strong> The distribution is right-skewed but progressively shifts towards forming a symmetrical bell curve as λ heavily scales upwards.</li>
</ul>
</div>

<div style="flex: 1;">
<h3 style="color: #334155;">5. Underlying Assumptions</h3>
<ul style="font-size: 1.1rem; color: #475569; line-height: 1.8;">
<li><strong>Independence:</strong> The occurrence of one event does not affect the probability of a second event.</li>
<li><strong>Proportionality:</strong> The average rate at which events occur strictly stays constant.</li>
<li><strong>Singularity:</strong> Two distinct events objectively cannot occur accurately at the exact same instant boundary.</li>
</ul>
</div>
</div>

<hr style="border-top: 1px dashed #cbd5e1; margin: 2rem 0;">

<h3 style="color: #334155;">6. Practical Real-Life Applications</h3>
<ul style="font-size: 1.1rem; color: #475569; line-height: 1.8;">
<li><b>Call Centers / Queuing Networks:</b> Determining the count of phone calls arriving at a customer support switchboard in one minute.</li>
<li><b>Traffic Analysis:</b> Calculating the probability of a given number of cars passing a toll booth within an hour.</li>
<li><b>Server Networking:</b> Assessing expected server overloads via analyzing data packet drops under fixed network conditions.</li>
<li><b>Retail Flow:</b> Estimating the count of customers passing through checkout lines per 15-minute intervals.</li>
<li><b>Manufacturing & Reliability:</b> Deciphering independent mechanical breakdowns or part defects linearly across extensive shifts.</li>
</ul>
</div>
""", unsafe_allow_html=True)
