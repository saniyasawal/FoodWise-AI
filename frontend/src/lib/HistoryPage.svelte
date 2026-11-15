
<script lang="ts">
    import { onMount } from 'svelte';
    import {
        History,
        Search,
        Trash2,
        CalendarDays,
        ClipboardList,
        Utensils,
        Info
    } from 'lucide-svelte';

    const API_BASE_URL =
        'https://foodwise-ai-api-88911246605.asia-south1.run.app';

    type HistoryRecord = {
        id: string;
        created_at: string;
        date: string;
        meals_served: number;
        kitchen_staff: number;
        temperature_C: number;
        humidity_percent: number;
        past_waste_kg: number;
        staff_experience: string;
        waste_category: string;
        special_event: number;
        predicted_food_waste_kg: number;
        unit: string;
        model: string;
    };

    let records = $state<HistoryRecord[]>([]);
    let searchQuery = $state('');
    let selectedCategory = $state('all');
    let loading = $state(true);
    let errorMessage = $state('');

    onMount(() => {
        loadHistory();
    });

    async function loadHistory() {
        loading = true;
        errorMessage = '';

        try {
            const response = await fetch(`${API_BASE_URL}/history`);

            if (!response.ok) {
                throw new Error('Unable to retrieve prediction history.');
            }

            const data = await response.json();

            records = data.history.map((item: any) => ({
                id: item.id,
                created_at: item.created_at,
                date: item.created_at,
                meals_served: item.input_data.meals_served,
                kitchen_staff: item.input_data.kitchen_staff,
                temperature_C: item.input_data.temperature_C,
                humidity_percent: item.input_data.humidity_percent,
                past_waste_kg: item.input_data.past_waste_kg,
                staff_experience: item.input_data.staff_experience,
                waste_category: item.input_data.waste_category,
                special_event: item.input_data.special_event,
                predicted_food_waste_kg: item.predicted_food_waste_kg,
                unit: item.unit,
                model: item.model
            }));
        } catch (error) {
            errorMessage =
                error instanceof Error
                    ? error.message
                    : 'Unable to connect to the history API.';
        } finally {
            loading = false;
        }
    }

    let filteredRecords = $derived(
        records.filter((record) => {
            const query = searchQuery.toLowerCase();

            const matchesSearch =
                record.date.toLowerCase().includes(query) ||
                record.waste_category.toLowerCase().includes(query) ||
                String(record.meals_served).includes(query);

            const matchesCategory =
                selectedCategory === 'all' ||
                record.waste_category.toLowerCase() === selectedCategory;

            return matchesSearch && matchesCategory;
        })
    );

    async function deleteRecord(id: string) {
        errorMessage = '';

        try {
            const response = await fetch(
                `${API_BASE_URL}/history/${encodeURIComponent(id)}`,
                { method: 'DELETE' }
            );

            if (!response.ok) {
                throw new Error('Unable to delete this prediction.');
            }

            records = records.filter((record) => record.id !== id);
        } catch (error) {
            errorMessage =
                error instanceof Error
                    ? error.message
                    : 'Unable to delete prediction.';
        }
    }

    async function clearHistory() {
        if (records.length === 0) return;

        if (
            window.confirm(
                'Are you sure you want to delete all prediction history?'
            )
        ) {
            errorMessage = '';

            try {
                const response = await fetch(`${API_BASE_URL}/history`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    throw new Error('Unable to clear prediction history.');
                }

                records = [];
            } catch (error) {
                errorMessage =
                    error instanceof Error
                        ? error.message
                        : 'Unable to clear prediction history.';
            }
        }
    }

    function formatDate(date: string) {
        return new Date(date).toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    }
</script>


<svelte:head>
    <title>Prediction History | FoodWise AI</title>
    <meta
        name="description"
        content="View and manage your saved food waste predictions."
    />
</svelte:head>

<section class="page history-page">
    <div class="page-header">
        <div>
            <div class="eyebrow">YOUR PREDICTION RECORDS</div>
            <h1>Prediction History</h1>
            <p>
                Review your previously generated food waste estimates.
            </p>
        </div>

        {#if records.length > 0}
            <button class="clear-button" onclick={clearHistory}>
                <Trash2 size={16} />
                Clear History
            </button>
        {/if}
    </div>

    <div class="stats-grid">
        <article class="stat-card">
            <div class="stat-icon"><ClipboardList size={20} /></div>
            <span class="stat-label">Total Predictions</span>
            <strong>{records.length}</strong>
            <small>Saved prediction records</small>
        </article>

        <article class="stat-card">
            <div class="stat-icon"><Utensils size={20} /></div>
            <span class="stat-label">Average Predicted Waste</span>
            <strong>
                {records.length
                    ? (records.reduce((sum, item) => sum + item.predicted_food_waste_kg, 0) / records.length).toFixed(2)
                    : '0.00'} kg
            </strong>
            <small>Across saved predictions</small>
        </article>

        <article class="stat-card">
            <div class="stat-icon"><History size={20} /></div>
            <span class="stat-label">Latest Prediction</span>
            <strong class="date-value">
                {records.length ? formatDate(records[0].date) : '—'}
            </strong>
            <small>Most recently saved record</small>
        </article>
    </div>

    <div class="history-card">
        <div class="history-heading">
            <div>
                <h2>Saved Predictions</h2>
                <p>{records.length} record(s) saved in Firestore</p>
            </div>
        </div>

        <div class="filters">
            <label class="search-box">
                <Search size={18} />
                <input
                    type="search"
                    placeholder="Search date, category or meals..."
                    bind:value={searchQuery}
                />
            </label>

            <select bind:value={selectedCategory} aria-label="Filter by food category">
                <option value="all">All Categories</option>
                <option value="vegetables">Vegetables</option>
                <option value="meat">Meat</option>
                <option value="dairy">Dairy</option>
                <option value="grains">Grains</option>
            </select>
        </div>

        {#if records.length === 0}
            <div class="empty-state">
                <div class="empty-icon"><History size={30} /></div>
                <h3>No predictions saved yet</h3>
                <p>
                    Generate a food waste prediction to see it recorded here.
                </p>
            </div>
        {:else if filteredRecords.length === 0}
            <div class="empty-state">
                <div class="empty-icon"><Search size={28} /></div>
                <h3>No matching predictions</h3>
                <p>Try changing your search or category filter.</p>
            </div>
        {:else}
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Saved Date</th>
                            <th>Meals Served</th>
                            <th>Category</th>
                            <th>Predicted Waste</th>
                            <th>Model</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {#each filteredRecords as record (record.id)}
                            <tr>
                                <td>
                                    <span class="date-cell">
                                        <CalendarDays size={15} />
                                        {formatDate(record.date)}
                                    </span>
                                </td>
                                <td>{record.meals_served}</td>
                                <td>
                                    <span class="category-pill">
                                        {record.waste_category}
                                    </span>
                                </td>
                                <td>
                                    <strong class="waste-value">
                                        {record.predicted_food_waste_kg.toFixed(2)} kg
                                    </strong>
                                </td>
                                <td>{record.model}</td>
                                <td>
                                    <button
                                        class="delete-button"
                                        onclick={() => deleteRecord(record.id)}
                                        aria-label="Delete this prediction"
                                        title="Delete prediction"
                                    >
                                        <Trash2 size={17} />
                                    </button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {/if}
    </div>

    <div class="history-note">
        <Info size={17} />
        <p>
    Prediction records are stored centrally in Google Cloud Firestore.
    The shared history is accessible across visitors and browsers.
       </p>
    </div>
</section>

<style>
    .history-page {
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
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
    .history-heading p {
        color: #747C75;
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
    }

    .clear-button,
    .delete-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 7px;
        border: 1px solid #F0D9D3;
        border-radius: 9px;
        background: white;
        color: #B64C3B;
        cursor: pointer;
    }

    .clear-button {
        padding: 10px 14px;
        font-size: 12px;
        font-weight: 650;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
    }

    .stat-card,
    .history-card {
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

    .stat-icon,
    .empty-icon {
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
        font-size: 23px;
    }

    .stat-card .date-value {
        font-size: 18px;
    }

    .stat-card small {
        color: #89918A;
        font-size: 11px;
    }

    .history-card {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .history-heading h2 {
        color: #18352A;
        font-size: 17px;
        margin: 0 0 6px;
    }

    .filters {
        display: flex;
        gap: 12px;
    }

    .search-box {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 12px;
        border: 1px solid #E2E9DF;
        border-radius: 9px;
        color: #89918A;
    }

    .search-box input {
        width: 100%;
        min-width: 0;
        border: 0;
        outline: 0;
        padding: 12px 0;
        color: #18352A;
        font: inherit;
        font-size: 13px;
        background: transparent;
    }

    .filters select {
        min-width: 155px;
        padding: 0 12px;
        border: 1px solid #E2E9DF;
        border-radius: 9px;
        color: #536157;
        background: white;
        font: inherit;
        font-size: 13px;
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
        padding: 13px 12px;
        background: #F7F9F5;
        color: #747C75;
        font-size: 12px;
        font-weight: 650;
    }

    td {
        padding: 15px 12px;
        border-bottom: 1px solid #EDF0EA;
        color: #536157;
        font-size: 13px;
    }

    td strong {
        color: #18352A;
    }

    .date-cell {
        display: inline-flex;
        align-items: center;
        gap: 7px;
    }

    .category-pill {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 20px;
        background: #F1F7E9;
        color: #287440;
        font-size: 11px;
        text-transform: capitalize;
    }

    .waste-value {
        color: #18352A;
    }

    .delete-button {
        width: 32px;
        height: 32px;
        border-color: transparent;
    }

    .delete-button:hover,
    .clear-button:hover {
        background: #FFF4F1;
    }

    .empty-state {
        padding: 45px 15px;
        text-align: center;
    }

    .empty-icon {
        width: 54px;
        height: 54px;
        margin: 0 auto 14px;
        border-radius: 14px;
    }

    .empty-state h3 {
        margin: 0 0 7px;
        color: #18352A;
        font-size: 16px;
    }

    .empty-state p {
        margin: 0;
        color: #747C75;
        font-size: 13px;
        line-height: 1.6;
    }

    .history-note {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 14px;
        border-radius: 10px;
        background: #F1F7E9;
        color: #287440;
    }

    .history-note p {
        margin: 0;
        color: #42634A;
        font-size: 12px;
        line-height: 1.6;
    }

    @media (max-width: 750px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }

        .page-header {
            align-items: flex-start;
            flex-direction: column;
        }

        .filters {
            flex-direction: column;
        }

        .filters select {
            min-height: 42px;
        }
    }
</style>
