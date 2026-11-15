
<script lang="ts">
    import {
        Leaf,
        Target,
        BrainCircuit,
        Database,
        Code2,
        ShieldCheck,
        TrendingUp,
        Lightbulb,
        BarChart3,
        Cloud
    } from 'lucide-svelte';
</script>

<svelte:head>
    <title>About | FoodWise AI</title>
    <meta
        name="description"
        content="Learn about FoodWise AI, its food waste prediction model, methodology and technology."
    />
</svelte:head>

<section class="page about-page">
    <div class="page-header">
        <div>
            <div class="eyebrow">ABOUT THE PROJECT</div>
            <h1>Making Food Management Smarter</h1>
            <p>
                Discover how FoodWise AI uses machine learning to help
                estimate food waste and support better kitchen decisions.
            </p>
        </div>
        <div class="hero-icon">
            <Leaf size={38} />
        </div>
    </div>

    <div class="about-hero">
        <div class="hero-content">
            <span class="hero-label">INTRODUCING FOODWISE AI</span>
            <h2>Predict today. Reduce waste tomorrow.</h2>
            <p>
                FoodWise AI is a machine-learning-based food waste prediction
                system. It estimates the quantity of food waste using
                operational factors such as meals served, kitchen staff,
                weather conditions, previous waste and food category.
            </p>
            <p>
                The goal is to provide useful estimates that can help
                kitchens plan food preparation, manage resources and make
                more informed decisions.
            </p>
        </div>
        <div class="hero-illustration">
            <div class="leaf-circle">
                <Leaf size={64} />
            </div>
            <span>Smarter food management</span>
        </div>
    </div>

    <div class="section-heading">
        <div>
            <div class="eyebrow">PROJECT OVERVIEW</div>
            <h2>What does FoodWise AI aim to achieve?</h2>
        </div>
    </div>

    <div class="overview-grid">
        <article class="info-card">
            <div class="card-icon"><Target size={22} /></div>
            <h3>Problem</h3>
            <p>
                Food waste can result from inaccurate meal planning,
                changing demand and inefficient resource allocation.
                Estimating waste in advance can help address these challenges.
            </p>
        </article>

        <article class="info-card">
            <div class="card-icon"><BrainCircuit size={22} /></div>
            <h3>AI Solution</h3>
            <p>
                A supervised machine learning model analyses historical
                operational data and predicts the expected food waste
                quantity in kilograms.
            </p>
        </article>

        <article class="info-card">
            <div class="card-icon"><TrendingUp size={22} /></div>
            <h3>Expected Benefit</h3>
            <p>
                Predictions can support better preparation planning,
                inventory decisions and awareness of factors associated
                with food waste.
            </p>
        </article>
    </div>

    <div class="section-heading">
        <div>
            <div class="eyebrow">MACHINE LEARNING</div>
            <h2>How the prediction system works</h2>
        </div>
    </div>

    <div class="method-card">
        <div class="method-step">
            <span class="step-number">01</span>
            <div>
                <h3>Data Collection</h3>
                <p>
                    Historical kitchen operational records are used,
                    including meals served, staffing, environmental
                    conditions and previous food waste.
                </p>
            </div>
        </div>

        <div class="method-step">
            <span class="step-number">02</span>
            <div>
                <h3>Data Preprocessing</h3>
                <p>
                    Missing values are handled, categorical values are
                    standardized, and date-based features are extracted.
                    The dataset is divided chronologically for training
                    and testing.
                </p>
            </div>
        </div>

        <div class="method-step">
            <span class="step-number">03</span>
            <div>
                <h3>Model Training</h3>
                <p>
                    Linear Regression, Random Forest and Gradient Boosting
                    are trained and evaluated using the same chronological
                    test dataset.
                </p>
            </div>
        </div>

        <div class="method-step">
            <span class="step-number">04</span>
            <div>
                <h3>Prediction</h3>
                <p>
                    The selected model receives user-provided kitchen
                    details through the application and returns an
                    estimated food waste quantity in kilograms.
                </p>
            </div>
        </div>
    </div>

    <div class="section-heading">
        <div>
            <div class="eyebrow">SELECTED MODEL</div>
            <h2>Linear Regression</h2>
            <p class="section-description">
                Selected because it achieved the best results among the
                three evaluated models on the held-out test dataset.
            </p>
        </div>
    </div>

    <div class="metrics-grid">
        <article class="metric-card">
            <span>Mean Absolute Error</span>
            <strong>4.8026 kg</strong>
            <small>Average absolute prediction error</small>
        </article>

        <article class="metric-card">
            <span>Root Mean Squared Error</span>
            <strong>7.3614 kg</strong>
            <small>Penalizes larger prediction errors</small>
        </article>

        <article class="metric-card">
            <span>R² Score</span>
            <strong>0.9203</strong>
            <small>Coefficient of determination</small>
        </article>
    </div>

    <div class="model-note">
        <Lightbulb size={19} />
        <p>
            These metrics describe performance on the project's held-out
            chronological test set. They do not guarantee the same accuracy
            on every future dataset or real-world kitchen.
        </p>
    </div>

    <div class="section-heading">
        <div>
            <div class="eyebrow">TECHNOLOGY STACK</div>
            <h2>Technologies behind FoodWise AI</h2>
        </div>
    </div>

    <div class="tech-grid">
        <article class="tech-card">
            <div class="tech-icon"><BrainCircuit size={21} /></div>
            <div>
                <h3>Machine Learning</h3>
                <p>Python, Pandas, NumPy and Scikit-learn</p>
            </div>
        </article>

        <article class="tech-card">
            <div class="tech-icon"><Database size={21} /></div>
            <div>
                <h3>Model Storage</h3>
                <p>Joblib for saving and loading the trained model</p>
            </div>
        </article>

        <article class="tech-card">
            <div class="tech-icon"><Code2 size={21} /></div>
            <div>
                <h3>Backend API</h3>
                <p>Python and FastAPI</p>
            </div>
        </article>

        <article class="tech-card">
            <div class="tech-icon"><Leaf size={21} /></div>
            <div>
                <h3>Frontend</h3>
                <p>SvelteKit and TypeScript</p>
            </div>
        </article>

        <article class="tech-card">
            <div class="tech-icon"><Cloud size={21} /></div>
            <div>
                <h3>Cloud Deployment</h3>
                <p>Google Cloud Run and Vercel</p>
            </div>
        </article>

        <article class="tech-card">
            <div class="tech-icon"><BarChart3 size={21} /></div>
            <div>
                <h3>Data Visualization</h3>
                <p>Matplotlib and Seaborn</p>
            </div>
        </article>
    </div>

    <div class="limitations-card">
        <ShieldCheck size={22} />
        <div>
            <h3>Understanding the predictions</h3>
            <p>
                FoodWise AI provides estimates based on patterns learned
                from the available historical dataset. Predictions are
                intended as decision-support information, not exact
                measurements or guaranteed outcomes. Prediction quality
                depends on the relevance and quality of the input data.
            </p>
        </div>
    </div>

    <footer class="about-footer">
        <Leaf size={18} />
        <span>FoodWise AI — Smarter decisions for a more sustainable future.</span>
    </footer>
</section>

<style>
    .about-page {
        display: flex;
        flex-direction: column;
        gap: 26px;
    }

    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
    }

    .eyebrow {
        color: #3B9B50;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1.2px;
    }

    .page-header h1 {
        margin: 7px 0;
        color: #18352A;
        font-size: 28px;
        font-weight: 750;
    }

    .page-header p,
    .section-description {
        max-width: 650px;
        margin: 0;
        color: #747C75;
        font-size: 14px;
        line-height: 1.7;
    }

    .hero-icon,
    .card-icon,
    .tech-icon {
        display: grid;
        place-items: center;
        flex-shrink: 0;
        background: #F1F7E9;
        color: #3B9B50;
        border-radius: 12px;
    }

    .hero-icon {
        width: 65px;
        height: 65px;
    }

    .about-hero {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        align-items: center;
        gap: 25px;
        padding: 32px;
        border-radius: 17px;
        background: #18352A;
        color: white;
    }

    .hero-label {
        color: #A9D7A9;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 1.4px;
    }

    .hero-content h2 {
        max-width: 500px;
        margin: 13px 0;
        font-size: 29px;
        line-height: 1.25;
    }

    .hero-content p {
        max-width: 590px;
        color: #D4E2D5;
        font-size: 13px;
        line-height: 1.8;
    }

    .hero-illustration {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
        color: #D4E2D5;
        font-size: 12px;
    }

    .leaf-circle {
        width: 145px;
        height: 145px;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: #DDEFCB;
        color: #287440;
    }

    .section-heading {
        margin-top: 4px;
    }

    .section-heading h2 {
        margin: 7px 0;
        color: #18352A;
        font-size: 20px;
    }

    .overview-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
    }

    .info-card,
    .method-card,
    .metric-card,
    .tech-card {
        border: 1px solid #E8EDE5;
        border-radius: 14px;
        background: white;
    }

    .info-card {
        padding: 21px;
    }

    .card-icon {
        width: 42px;
        height: 42px;
        margin-bottom: 14px;
    }

    .info-card h3,
    .tech-card h3,
    .method-step h3,
    .limitations-card h3 {
        margin: 0 0 8px;
        color: #18352A;
        font-size: 14px;
    }

    .info-card p,
    .method-step p,
    .tech-card p,
    .limitations-card p {
        margin: 0;
        color: #747C75;
        font-size: 12px;
        line-height: 1.8;
    }

    .method-card {
        padding: 8px 23px;
    }

    .method-step {
        display: flex;
        gap: 18px;
        padding: 19px 0;
        border-bottom: 1px solid #EDF0EA;
    }

    .method-step:last-child {
        border-bottom: 0;
    }

    .step-number {
        width: 35px;
        height: 35px;
        display: grid;
        place-items: center;
        flex-shrink: 0;
        border-radius: 10px;
        background: #F1F7E9;
        color: #287440;
        font-size: 12px;
        font-weight: 750;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
    }

    .metric-card {
        display: flex;
        flex-direction: column;
        gap: 9px;
        padding: 21px;
    }

    .metric-card span {
        color: #747C75;
        font-size: 12px;
    }

    .metric-card strong {
        color: #18352A;
        font-size: 25px;
    }

    .metric-card small {
        color: #89918A;
        font-size: 11px;
    }

    .model-note,
    .limitations-card {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 16px;
        border-radius: 11px;
        background: #F1F7E9;
        color: #287440;
    }

    .model-note p {
        margin: 0;
        color: #42634A;
        font-size: 12px;
        line-height: 1.7;
    }

    .tech-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 13px;
    }

    .tech-card {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 17px;
    }

    .tech-icon {
        width: 42px;
        height: 42px;
    }

    .tech-card h3 {
        margin-bottom: 5px;
    }

    .limitations-card {
        background: #F7F9F5;
        color: #3B9B50;
    }

    .limitations-card h3 {
        margin-bottom: 6px;
    }

    .about-footer {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 9px;
        padding: 17px;
        color: #287440;
        font-size: 12px;
        font-weight: 600;
    }

    @media (max-width: 750px) {
        .about-hero {
            grid-template-columns: 1fr;
        }

        .hero-illustration {
            padding: 15px 0;
        }

        .overview-grid,
        .metrics-grid {
            grid-template-columns: 1fr;
        }

        .tech-grid {
            grid-template-columns: 1fr;
        }

        .page-header {
            align-items: flex-start;
        }

        .page-header h1 {
            font-size: 23px;
        }
    }
</style>
