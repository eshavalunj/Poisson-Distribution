# Poisson Distribution Simulator

An advanced Python-based interactive simulation of the Poisson Distribution, built with Streamlit.
This project visualizes the mathematical foundation of probability and showcases how events occur independently over a fixed continuous interval.

![pd1](https://github.com/user-attachments/assets/29906a57-49f9-4347-95e3-61a667a9ba7c)


## 🌟 Features
- **Interactive Controls:** Sliders and inputs for the average rate ($\lambda$) and sample size.
- **Compare Mode:** Allows comparing two different Poisson distributions ($\lambda$ vs $\lambda_2$) side-by-side.
- **3D & 2D Visualizations:** View the theoretical Probability Mass Function (PMF) and simulated Data Histograms in an attractive 3D space or standard 2D view.
- **Dynamically Calculated Statistics:** Real-time metrics comparing Theoretical Mean/Variance against Simulated Data.
- **Responsive UI:** Clean layout with structured tables, stylish customized widgets, and interpretation blocks.
- **Export Options:** Instantly download visualization plots as high-quality PNGs.

## 📘 Introduction to Poisson Distribution
The Poisson distribution is a discrete probability distribution that expresses the probability of a given number of events occurring in a fixed interval of time or space if these events occur with a known constant mean rate and independently of the time since the last event.

### Mathematical Formula
The probability of observing $k$ events in an interval is given by the equation:

$$ P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!} $$

Where:
- $\lambda$ (Lambda) is the average number of events in the given time interval.
- $k$ is the number of occurrences of an event.
- $e$ is Euler's number ($e \approx 2.71828$).
- $k!$ is the factorial of $k$.

### Properties
- The **Mean** ($\mu$) is $\lambda$.
- The **Variance** ($\sigma^2$) is also $\lambda$. This is a unique and fundamental property of the Poisson distribution.

## 🛠 Features Implementation
1. **Core Logic:** We utilize Python's `scipy.stats.poisson` to accurately calculate the theoretical Probability Mass Function (PMF).
2. **Simulation:** We generate pseudo-random variables shaped by the Poisson distribution using `numpy.random.poisson`.
3. **Visualization:** Complex and attractive dual-mode visualizations are built using `matplotlib` and `mpl_toolkits.mplot3d`, seamlessly deployed within Streamlit to achieve immediate reactivity.
4. **Error Handling & State Validation:** The Streamlit widgets cleanly parse and constrain negative/invalid $\lambda$ parameters dynamically.

## 🚀 How to Run the Project

### Prerequisites
Make sure you have Python installed. The required libraries are defined below:
- `streamlit`
- `numpy`
- `matplotlib`
- `scipy`

### Step 1: Install Dependencies
Open your terminal (or Command Prompt) and run:
```bash
pip install streamlit numpy matplotlib scipy
```

### Step 2: Run the Streamlit Application
Navigate to the project directory containing `app.py`:
```bash
streamlit run app.py
```

### Step 3: Use the web application
Once Streamlit starts the local server, your default web browser will open (usually `http://localhost:8501`) exhibiting the dashboard.

## 📊 Conclusion
This interactive simulator is a powerful academic and practical tool bridging the gap between theoretical statistics and visual intuition. By manipulating parameters dynamically, users can directly observe:
- How lower values of $\lambda$ make the distribution highly asymmetrical (right-skewed).
- How the distribution morphs into a nearly symmetric bell curve as $\lambda$ grows continuously, perfectly paralleling the Normal distribution.
- The Law of Large Numbers, actively demonstrated as the simulated sample histogram aligns tighter with the theoretical PMF at extremely large trial counts.

This makes the tool outstanding for pedagogical use or exploratory data analysis in queueing theory, reliability engineering, and risk modeling.
