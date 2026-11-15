
<script lang="ts">
    import {
        ArrowRight,
        CalendarDays,
        Check,
        CloudSun,
        Droplets,
        Info,
        Leaf,
        Lightbulb,
        LoaderCircle,
        Sparkles,
        Thermometer,
        TrendingDown,
        Utensils,
        Users
    } from 'lucide-svelte';

    type PredictionResult = {
        predicted_food_waste_kg: number;
        unit: string;
        model: string;
    };

    function todayString() {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    let form = $state({
        meals_served: '500',
        kitchen_staff: '8',
        temperature_C: '28.5',
        humidity_percent: '65',
        past_waste_kg: '18.5',
        staff_experience: 'intermediate',
        waste_category: 'vegetables',
        special_event: false,
        date: todayString()
    });

    let loading = $state(false);
    let result = $state<PredictionResult | null>(null);
    let errorMessage = $state('');

    const days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ];

    let selectedDate = $derived(
        form.date ? new Date(`${form.date}T00:00:00`) : null
    );

    let selectedDay = $derived(
        selectedDate ? days[(selectedDate.getDay() + 6) % 7] : ''
    );

    let selectedMonth = $derived(
        selectedDate
            ? selectedDate.toLocaleDateString('en-US', { month: 'long' })
            : '—'
    );

    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();

        errorMessage = '';
        result = null;

        if (!form.date) {
            errorMessage = 'Please select a prediction date.';
            return;
        }

        if (
            !form.meals_served ||
            Number(form.meals_served) <= 0 ||
            !form.kitchen_staff ||
            Number(form.kitchen_staff) < 0 ||
            !form.temperature_C ||
            !form.humidity_percent ||
            Number(form.humidity_percent) < 0 ||
            Number(form.humidity_percent) > 100 ||
            !form.past_waste_kg ||
            Number(form.past_waste_kg) < 0
        ) {
            errorMessage = 'Please check the entered values and try again.';
            return;
        }

        const date = new Date(`${form.date}T00:00:00`);

        const payload = {
            meals_served: Number(form.meals_served),
            kitchen_staff: Number(form.kitchen_staff),
            temperature_C: Number(form.temperature_C),
            humidity_percent: Number(form.humidity_percent),
            day_of_week: (date.getDay() + 6) % 7,
            special_event: form.special_event ? 1 : 0,
            past_waste_kg: Number(form.past_waste_kg),
            staff_experience: form.staff_experience,
            waste_category: form.waste_category,
            month: date.getMonth() + 1,
            day_of_month: date.getDate()
        };

        loading = true;

        try {
            const response = await fetch('https://foodwise-ai-api-88911246605.asia-south1.run.app/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail
                        ? typeof data.detail === 'string'
                            ? data.detail
                            : JSON.stringify(data.detail)
                        : 'Prediction request failed.'
                );
            }

            result = data;
            
        } catch (error) {
            errorMessage =
                error instanceof Error
                    ? error.message
                    : 'Unable to connect to the prediction API.';

        } finally {
            loading = false;
        }
    }

    function resetForm() {
        form = {
            meals_served: '',
            kitchen_staff: '',
            temperature_C: '',
            humidity_percent: '',
            past_waste_kg: '',
            staff_experience: 'intermediate',
            waste_category: 'vegetables',
            special_event: false,
            date: todayString()
        };

        result = null;
        errorMessage = '';
    }
</script>

<div class="page prediction-page">
    <div class="page-header">
        <div>
            <div class="eyebrow">AI WASTE ESTIMATOR</div>
            <h1>Predict Your Kitchen’s Food Waste</h1>
            <p>
                Enter your daily kitchen details to estimate the amount of
                food waste generated.
            </p>
        </div>
    </div>

    {#if loading}
        <section class="card loading-panel">
            <LoaderCircle size={34} />
            <h2>Preparing your prediction…</h2>
            <p>
                Your kitchen information is being processed by the
                Linear Regression model.
            </p>
        </section>
    {:else if result}
        <section class="result-hero">
            <div class="success-mark">
                <Check size={28} />
            </div>

            <span class="result-label">PREDICTED FOOD WASTE</span>

            <div class="result-number">
                {result.predicted_food_waste_kg.toFixed(2)}
                <span>{result.unit}</span>
            </div>

            <p>Estimated for {form.date}</p>

            <div class="result-meta">
                <div>
                    <Sparkles size={18} />
                    <span>
                        Model used
                        <strong>{result.model}</strong>
                    </span>
                </div>
                <div>
                    <Check size={18} />
                    <span>
                        Prediction status
                        <strong>Successful</strong>
                    </span>
                </div>
                <div>
                    <Leaf size={18} />
                    <span>
                        Waste category
                        <strong>{form.waste_category}</strong>
                    </span>
                </div>
            </div>
        </section>

        <section class="card understanding-card">
            <h3>Understanding your prediction</h3>
            <p>
                The model used your kitchen operations, environmental
                conditions, previous-cycle waste and food category
                to calculate this estimate.
            </p>
        </section>

        <div class="form-actions">
            <button class="button secondary" onclick={resetForm}>
                New Prediction
            </button>
        </div>
    {:else}
        <div class="prediction-layout">
            <form class="prediction-form" onsubmit={handleSubmit}>
                {#if errorMessage}
                    <div class="error-banner">
                        <Info size={19} />
                        <div>
                            <strong>Unable to generate prediction</strong>
                            <span>{errorMessage}</span>
                        </div>
                    </div>
                {/if}

                <section class="form-section">
                    <div class="section-heading">
                        <div class="section-icon">
                            <Utensils size={19} />
                        </div>
                        <div>
                            <span>SECTION A</span>
                            <h3>Kitchen Operations</h3>
                            <p>Tell us about the scale and experience of your kitchen team.</p>
                        </div>
                    </div>

                    <div class="fields-grid">
                        <label class="field">
                            <span>Meals Served</span>
                            <div class="input-wrap">
                                <Utensils size={18} />
                                <input
                                    type="number"
                                    min="1"
                                    required
                                    bind:value={form.meals_served}
                                />
                            </div>
                            <small>Total meals prepared for guests</small>
                        </label>

                        <label class="field">
                            <span>Kitchen Staff</span>
                            <div class="input-wrap">
                                <Users size={18} />
                                <input
                                    type="number"
                                    min="0"
                                    required
                                    bind:value={form.kitchen_staff}
                                />
                            </div>
                            <small>People working this service</small>
                        </label>

                        <label class="field">
                            <span>Staff Experience</span>
                            <div class="input-wrap select-wrap">
                                <Sparkles size={18} />
                                <select bind:value={form.staff_experience}>
                                    <option value="beginner">Beginner</option>
                                    <option value="intermediate">Intermediate</option>
                                    <option value="expert">Expert</option>
                                    <option value="unknown">Unknown</option>
                                </select>
                            </div>
                            <small>Average team experience level</small>
                        </label>
                    </div>
                </section>

                <section class="form-section">
                    <div class="section-heading">
                        <div class="section-icon">
                            <CloudSun size={19} />
                        </div>
                        <div>
                            <span>SECTION B</span>
                            <h3>Environmental Conditions</h3>
                            <p>Add conditions that may affect food handling and storage.</p>
                        </div>
                    </div>

                    <div class="fields-grid">
                        <label class="field">
                            <span>Temperature</span>
                            <div class="input-wrap">
                                <Thermometer size={18} />
                                <input
                                    type="number"
                                    step="0.1"
                                    required
                                    bind:value={form.temperature_C}
                                />
                                <b>°C</b>
                            </div>
                            <small>Average kitchen temperature</small>
                        </label>

                        <label class="field">
                            <span>Humidity</span>
                            <div class="input-wrap">
                                <Droplets size={18} />
                                <input
                                    type="number"
                                    min="0"
                                    max="100"
                                    step="0.1"
                                    required
                                    bind:value={form.humidity_percent}
                                />
                                <b>%</b>
                            </div>
                            <small>Relative humidity (0–100%)</small>
                        </label>

                        <div class="derived-field">
                            <span>Day of Week</span>
                            <strong>{selectedDay || '—'}</strong>
                            <small>Derived from selected date</small>
                        </div>

                        <label class="field toggle-field">
                            <span>Special Event</span>
                            <div class="toggle-row">
                                <input
                                    type="checkbox"
                                    bind:checked={form.special_event}
                                />
                                <b>{form.special_event ? 'Yes, special event' : 'No special event'}</b>
                            </div>
                            <small>Events may change expected meal volume</small>
                        </label>
                    </div>
                </section>

                <section class="form-section">
                    <div class="section-heading">
                        <div class="section-icon">
                            <Leaf size={19} />
                        </div>
                        <div>
                            <span>SECTION C</span>
                            <h3>Food Waste Information</h3>
                            <p>Use the most recent completed kitchen cycle as context.</p>
                        </div>
                    </div>

                    <div class="fields-grid">
                        <label class="field">
                            <span>Previous Cycle Food Waste</span>
                            <div class="input-wrap">
                                <TrendingDown size={18} />
                                <input
                                    type="number"
                                    min="0"
                                    step="0.01"
                                    required
                                    bind:value={form.past_waste_kg}
                                />
                                <b>kg</b>
                            </div>
                            <small>Your latest measured waste total</small>
                        </label>

                        <label class="field">
                            <span>Waste Category</span>
                            <div class="input-wrap select-wrap">
                                <Leaf size={18} />
                                <select bind:value={form.waste_category}>
                                    <option value="meat">Meat</option>
                                    <option value="dairy">Dairy</option>
                                    <option value="vegetables">Vegetables</option>
                                    <option value="grains">Grains</option>
                                </select>
                            </div>
                            <small>Main category being estimated</small>
                        </label>
                    </div>
                </section>

                <section class="form-section">
                    <div class="section-heading">
                        <div class="section-icon">
                            <CalendarDays size={19} />
                        </div>
                        <div>
                            <span>SECTION D</span>
                            <h3>Prediction Date</h3>
                            <p>Choose the operational date for this estimate.</p>
                        </div>
                    </div>

                    <div class="fields-grid">
                        <label class="field">
                            <span>Date</span>
                            <div class="input-wrap">
                                <CalendarDays size={18} />
                                <input
                                    type="date"
                                    required
                                    bind:value={form.date}
                                />
                            </div>
                            <small>Choose the date for your prediction</small>
                        </label>

                        <div class="derived-field">
                            <span>Derived Month</span>
                            <strong>{selectedMonth}</strong>
                            <small>From selected date</small>
                        </div>

                        <div class="derived-field">
                            <span>Day of Month</span>
                            <strong>{selectedDate ? selectedDate.getDate() : '—'}</strong>
                            <small>From selected date</small>
                        </div>
                    </div>
                </section>

                <div class="form-actions">
                    <div>
                        <Info size={16} />
                        <span>Your inputs are sent to the FoodWise prediction API.</span>
                    </div>

                    <button
                        type="button"
                        class="button secondary"
                        onclick={resetForm}
                    >
                        Reset Form
                    </button>

                    <button type="submit" class="button primary">
                        <Sparkles size={17} />
                        Predict Food Waste
                    </button>
                </div>
            </form>

            <aside class="prediction-aside">
                <div class="aside-card">
                    <span>HOW IT WORKS</span>
                    <h3>From kitchen details to a clear estimate</h3>
                    <ol>
                        <li>
                            <i>1</i>
                            <div>
                                <strong>Enter your kitchen details</strong>
                                <span>Provide operational and environmental information.</span>
                            </div>
                        </li>
                        <li>
                            <i>2</i>
                            <div>
                                <strong>Let the model calculate</strong>
                                <span>Your inputs are processed by the trained regression model.</span>
                            </div>
                        </li>
                        <li>
                            <i>3</i>
                            <div>
                                <strong>Review your estimate</strong>
                                <span>Use the result to support food planning.</span>
                            </div>
                        </li>
                    </ol>
                </div>

                <div class="tip-card">
                    <Lightbulb size={20} />
                    <div>
                        <strong>For a useful estimate</strong>
                        <p>Use measured values from a typical completed service whenever possible.</p>
                    </div>
                </div>
            </aside>
        </div>
    {/if}
</div>
