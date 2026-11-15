
<script lang="ts">
    import {
        BarChart3,
        TrendingUp,
        Target,
        Award,
        CheckCircle2,
        Info
    } from 'lucide-svelte';

    const models = [
        {
            name: 'Linear Regression',
            mae: 4.8026,
            rmse: 7.3614,
            r2: 0.9203,
            selected: true
        },
        {
            name: 'Random Forest',
            mae: 5.4281,
            rmse: 8.4119,
            r2: 0.8959,
            selected: false
        },
        {
            name: 'Gradient Boosting',
            mae: 5.0024,
            rmse: 8.4497,
            r2: 0.8949,
            selected: false
        }
    ];

    const features = [
        { name: 'Meals Served', correlation: 0.8521 },
        { name: 'Past Waste', correlation: 0.2608 },
        { name: 'Special Event', correlation: 0.1188 },
        { name: 'Day of Week', correlation: 0.0081 },
        { name: 'Kitchen Staff', correlation: 0.0072 },
        { name: 'Temperature', correlation: -0.0159 },
        { name: 'Humidity', correlation: -0.0218 }
    ];

    const bestModel = models[0];
</script>

<svelte:head>
    <title>Analytics & Insights | FoodWise AI</title>
    <meta
        name="description"
        content="Explore FoodWise AI model performance and dataset insights."
    />
</svelte:head>

<section class="page">
    <div class="page-header">
        <div>
            <span class="eyebrow">MODEL PERFORMANCE</span>
            <h1>Analytics & Insights</h1>
            <p>
                Understand how the food waste prediction model performs
                and explore patterns in the training dataset.
            </p>
        </div>
    </div>

    <div class="stats-grid">
        <article class="stat-card">
            <div class="stat-icon"><Target size={20} /></div>
            <span class="stat-label">Mean Absolute Error</span>
            <strong>{bestModel.mae.toFixed(2)} kg</strong>
            <small>Average absolute prediction error</small>
        </article>

        <article class="stat-card">
            <div class="stat-icon"><BarChart3 size={20} /></div>
            <span class="stat-label">Root Mean Squared Error</span>
            <strong>{bestModel.rmse.toFixed(2)} kg</strong>
            <small>Penalizes larger prediction errors</small>
        </article>

        <article class="stat-card">
            <div class="stat-icon"><TrendingUp size={20} /></div>
            <span class="stat-label">R² Score</span>
            <strong>{(bestModel.r2 * 100).toFixed(2)}%</strong>
            <small>Variance explained on the test set</small>
        </article>

        <article class="stat-card">
            <div class="stat-icon"><Award size={20} /></div>
            <span class="stat-label">Selected Model</span>
            <strong>Linear Regression</strong>
            <small>Best overall test-set performance</small>
        </article>
    </div>

    <article class="analytics-card">
        <div class="card-heading">
            <div>
                <h2>Model Performance Comparison</h2>
                <p>Evaluation on the chronological test dataset (174 records).</p>
            </div>
        </div>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>MAE (kg)</th>
                        <th>RMSE (kg)</th>
                        <th>R² Score</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {#each models as model}
                        <tr>
                            <td><strong>{model.name}</strong></td>
                            <td>{model.mae.toFixed(4)}</td>
                            <td>{model.rmse.toFixed(4)}</td>
                            <td>{model.r2.toFixed(4)}</td>
                            <td>
                                {#if model.selected}
                                    <span class="selected-label">
                                        <CheckCircle2 size={14} />
                                        Selected
                                    </span>
                                {:else}
                                    <span class="other-label">Compared</span>
                                {/if}
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </article>

    <article class="analytics-card">
        <div class="card-heading">
            <div>
                <h2>Feature Correlation with Food Waste</h2>
                <p>
                    Pearson correlation values calculated from the training
                    dataset. These indicate linear association, not causation.
                </p>
            </div>
        </div>

        <div class="correlation-list">
            {#each features as feature}
                <div class="correlation-row">
                    <div class="correlation-info">
                        <span>{feature.name}</span>
                        <strong>{feature.correlation.toFixed(4)}</strong>
                    </div>
                    <div class="correlation-track">
                        <div
                            class:negative={feature.correlation < 0}
                            class="correlation-fill"
                            style={`width: ${Math.abs(feature.correlation) * 100}%;`}
                        ></div>
                    </div>
                </div>
            {/each}
        </div>

        <div class="insight-note">
            <Info size={18} />
            <p>
                Meals served has the strongest positive linear correlation
                with food waste (0.8521). This suggests that higher meal
                volumes are associated with higher food waste in this dataset.
            </p>
        </div>
    </article>

    <article class="analytics-card selection-card">
        <div class="selection-icon"><Award size={24} /></div>
        <div>
            <span class="eyebrow">MODEL SELECTION</span>
            <h2>Why Linear Regression?</h2>
            <p>
                Linear Regression achieved the lowest MAE (4.8026 kg),
                lowest RMSE (7.3614 kg), and highest R² score (0.9203)
                among the three evaluated models on the chronological
                test set.
            </p>
            <p>
                It was selected because it delivered the best measured
                performance while remaining simpler and easier to interpret
                than the tree-based alternatives.
            </p>
        </div>
    </article>

    <p class="analytics-disclaimer">
        Metrics are based on the model evaluation performed during training.
        They are not live performance measurements from user predictions.
    </p>
</section>

<style>
    .page {
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }

    .page-header h1 {
        margin: 7px 0;
        color: #18352A;
        font-size: 28px;
        font-weight: 750;
    }

    .page-header p,
    .card-heading p {
        color: #747C75;
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
    }

    .eyebrow {
        color: #3B9B50;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1.2px;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
    }

    .stat-card,
    .analytics-card {
        background: white;
        border: 1px solid #E8EDE5;
        border-radius: 15px;
        padding: 20px;
    }

    .stat-card {
        display: flex;
        flex-direction: column;
        gap: 9px;
    }

    .stat-icon {
        width: 38px;
        height: 38px;
        display: grid;
        place-items: center;
        background: #F1F7E9;
        color: #3B9B50;
        border-radius: 10px;
    }

    .stat-label {
        color: #747C75;
        font-size: 12px;
    }

    .stat-card strong {
        color: #18352A;
        font-size: 22px;
        line-height: 1.3;
    }

    .stat-card small {
        color: #89918A;
        font-size: 11px;
    }

    .analytics-card {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .card-heading h2,
    .selection-card h2 {
        color: #18352A;
        font-size: 17px;
        margin: 0 0 6px;
    }

    .table-wrap {
        width: 100%;
        overflow-x: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
        white-space: nowrap;
    }

    th {
        color: #747C75;
        background: #F7F9F5;
        font-size: 12px;
        font-weight: 650;
    }

    th, td {
        padding: 14px 12px;
        border-bottom: 1px solid #EDF0EA;
    }

    td {
        color: #536157;
        font-size: 13px;
    }

    td strong {
        color: #18352A;
    }

    .selected-label {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        color: #258044;
        font-size: 12px;
        font-weight: 700;
    }

    .other-label {
        color: #89918A;
        font-size: 12px;
    }

    .correlation-list {
        display: flex;
        flex-direction: column;
        gap: 17px;
    }

    .correlation-info {
        display: flex;
        justify-content: space-between;
        margin-bottom: 7px;
        color: #536157;
        font-size: 13px;
    }

    .correlation-info strong {
        color: #18352A;
        font-variant-numeric: tabular-nums;
    }

    .correlation-track {
        height: 9px;
        background: #F0F3ED;
        border-radius: 20px;
        overflow: hidden;
    }

    .correlation-fill {
        height: 100%;
        background: #3B9B50;
        border-radius: 20px;
        min-width: 2px;
    }

    .correlation-fill.negative {
        background: #F47B20;
    }

    .insight-note {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 14px;
        background: #F1F7E9;
        border-radius: 10px;
        color: #287440;
    }

    .insight-note p {
        margin: 0;
        color: #42634A;
        font-size: 13px;
        line-height: 1.6;
    }

    .selection-card {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 16px;
        background: #FBF9F2;
    }

    .selection-icon {
        flex-shrink: 0;
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 12px;
        color: #F47B20;
        background: #FFF0DF;
    }

    .selection-card p {
        color: #667269;
        font-size: 13px;
        line-height: 1.7;
        margin: 8px 0 0;
    }

    .analytics-disclaimer {
        color: #89918A;
        font-size: 11px;
        line-height: 1.5;
        margin: 0;
    }

    @media (max-width: 1050px) {
        .stats-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 600px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }

        .stat-card,
        .analytics-card {
            padding: 16px;
        }

        .page-header h1 {
            font-size: 23px;
        }
    }
</style>
