
<script lang="ts">
    import {
        ArrowRight,
        BarChart3,
        Bell,
        CalendarDays,
        Check,
        ClipboardList,
        History,
        Info,
        LayoutDashboard,
        Leaf,
        Menu,
        Plus,
        Settings2,
        Sparkles,
        Sprout,
        TrendingDown,
        TrendingUp,
        Utensils,
        Users,
        X
    } from 'lucide-svelte';

    import PredictionPage from '#lib/PredictionPage.svelte';
    import AnalyticsPage from '#lib/AnalyticsPage.svelte';
    import HistoryPage from '#lib/HistoryPage.svelte';
    import AboutPage from '#lib/AboutPage.svelte';

    type Page = 'dashboard' | 'prediction' | 'analytics' | 'history' | 'about';

    let page = $state<Page>('dashboard');
    let mobileOpen = $state(false);

    const navItems = [
        { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { id: 'prediction', label: 'Waste Prediction', icon: Sparkles },
        { id: 'analytics', label: 'Analytics & Insights', icon: BarChart3 },
        { id: 'history', label: 'Prediction History', icon: History },
        { id: 'about', label: 'About the Project', icon: Info }
    ];

    const cards = [
        {
            label: 'Total predictions',
            value: '84',
            detail: '+12 this month',
            icon: ClipboardList,
            tone: 'green'
        },
        {
            label: 'Average food waste',
            value: '16.8',
            suffix: 'kg',
            detail: '−8.4% vs last month',
            icon: TrendingDown,
            tone: 'sage'
        },
        {
            label: 'Lowest prediction',
            value: '7.24',
            suffix: 'kg',
            detail: 'May 4 · Grains',
            icon: TrendingDown,
            tone: 'orange'
        },
        {
            label: 'Highest prediction',
            value: '28.6',
            suffix: 'kg',
            detail: 'May 9 · Meat',
            icon: TrendingUp,
            tone: 'cream'
        }
    ];

    const historyRows = [
        {
            id: 'FW-1084',
            date: 'May 14, 2025',
            meals: 240,
            category: 'Vegetables',
            waste: '16.42'
        },
        {
            id: 'FW-1083',
            date: 'May 13, 2025',
            meals: 185,
            category: 'Grains',
            waste: '12.08'
        },
        {
            id: 'FW-1082',
            date: 'May 12, 2025',
            meals: 320,
            category: 'Meat',
            waste: '24.71'
        }
    ];

    const bars = [
        { name: 'Vegetables', value: 82, kg: '24.8', color: '#176B3A' },
        { name: 'Meat', value: 66, kg: '19.9', color: '#3B9B50' },
        { name: 'Dairy', value: 47, kg: '14.2', color: '#8FC46C' },
        { name: 'Grains', value: 35, kg: '10.6', color: '#F47B20' }
    ];

    function navigate(id: Page) {
        page = id;
        mobileOpen = false;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
</script>

<div class="app-shell">
    <aside class:mobile-open={mobileOpen} class="sidebar">
        <div class="sidebar-top">
            <button
                class="mobile-close"
                onclick={() => mobileOpen = false}
                aria-label="Close menu"
            >
                <X size={20} />
            </button>

            <div class="brand">
                <div class="brand-mark" aria-hidden="true">
                    <Leaf size={23} strokeWidth={2.7} />
                </div>

                <div>
                    <div class="brand-name">FoodWise <span>AI</span></div>
                    <div class="brand-tag">Smarter kitchens. Less waste.</div>
                </div>
            </div>

            <nav class="nav-list" aria-label="Main navigation">
                <div class="nav-label">WORKSPACE</div>

                {#each navItems as item}
                    <button
                        class:active={page === item.id}
                        class="nav-item"
                        onclick={() => navigate(item.id as Page)}
                    >
                        <item.icon size={19} />
                        <span>{item.label}</span>
                    </button>
                {/each}
            </nav>
        </div>

        <div class="sidebar-impact">
            <div class="impact-icon">
                <Sprout size={20} />
            </div>

            <div>
                <strong>Kitchen impact</strong>
                <span>128 kg less waste this month</span>
            </div>

            <div class="impact-bar"><span></span></div>
            <small>Sample sustainability goal</small>
        </div>

        <div class="sidebar-user">
            <div class="avatar">KM</div>

            <div>
                <strong>Kitchen Manager</strong>
                <span>Greenfork Kitchen</span>
            </div>

            <Settings2 size={17} />
        </div>
    </aside>

    {#if mobileOpen}
        <button
            class="sidebar-scrim"
            onclick={() => mobileOpen = false}
            aria-label="Close menu"
        ></button>
    {/if}

    <div class="main-area">
        <header class="topbar">
            <button
                class="menu-button"
                onclick={() => mobileOpen = true}
                aria-label="Open menu"
            >
                <Menu size={22} />
            </button>

            <div class="mobile-brand">
                <div class="brand-mark">
                    <Leaf size={23} />
                </div>
                <strong>FoodWise AI</strong>
            </div>

            <div class="topbar-actions">
                <span class="sample-badge">
                    <span></span> Prototype mode
                </span>

                <button class="icon-button" aria-label="Notifications">
                    <Bell size={19} />
                    <i></i>
                </button>

                <div class="top-avatar">KM</div>
            </div>
        </header>

        <main>
            {#if page === 'dashboard'}

                <section class="page">
                    <div class="page-header">
                        <div>
                            <div class="eyebrow">KITCHEN OVERVIEW</div>
                            <h1>Good morning, Kitchen Manager!</h1>
                            <p>
                                Here's what's happening with your kitchen's food waste.
                            </p>
                        </div>

                        <button
                            class="primary-button"
                            onclick={() => navigate('prediction')}
                        >
                            <Plus size={18} />
                            New prediction
                        </button>
                    </div>

                    <div class="stats-grid">
                        {#each cards as card}
                            <div class="stat-card">
                                <div class="stat-card-top">
                                    <span>{card.label}</span>
                                    <div class="stat-icon {card.tone}">
                                        <card.icon size={20} />
                                    </div>
                                </div>

                                <div class="stat-value">
                                    {card.value}
                                    {#if card.suffix}
                                        <span>{card.suffix}</span>
                                    {/if}
                                </div>

                                <div class="stat-detail">{card.detail}</div>
                            </div>
                        {/each}
                    </div>

                    <div class="dashboard-hero">
                        <div class="hero-content">
                            <span class="hero-tag">
                                <Sparkles size={15} />
                                SMART FOOD MANAGEMENT
                            </span>

                            <h2>Make every meal count.</h2>

                            <p>
                                Use AI-powered predictions to estimate food waste
                                before it happens. Make smarter kitchen decisions
                                and reduce unnecessary food waste.
                            </p>

                            <button
                                class="hero-button"
                                onclick={() => navigate('prediction')}
                            >
                                Predict food waste
                                <ArrowRight size={17} />
                            </button>
                        </div>

                        <div class="hero-image"></div>
                    </div>

                    <div class="dashboard-grid">
                        <div class="dashboard-panel trend-panel">
                            <div class="panel-heading">
                                <div>
                                    <h3>Food waste overview</h3>
                                    <p>Illustrative monthly waste trend</p>
                                </div>

                                <span class="period-label">
                                    <CalendarDays size={15} />
                                    Monthly
                                </span>
                            </div>

                            <div class="trend-summary">
                                <strong>16.8 kg</strong>
                                <span>
                                    <TrendingDown size={15} />
                                    8.4% lower
                                </span>
                            </div>

                            <div class="trend-chart">
                                <div class="chart-y-labels">
                                    <span>30 kg</span>
                                    <span>20 kg</span>
                                    <span>10 kg</span>
                                    <span>0 kg</span>
                                </div>

                                <div class="chart-area">
                                    <div class="chart-grid-lines">
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>

                                    <svg
                                        viewBox="0 0 600 180"
                                        preserveAspectRatio="none"
                                        role="img"
                                        aria-label="Illustrative food waste trend chart"
                                    >
                                        <defs>
                                            <linearGradient
                                                id="chartFill"
                                                x1="0"
                                                y1="0"
                                                x2="0"
                                                y2="1"
                                            >
                                                <stop
                                                    offset="0%"
                                                    stop-color="#3B9B50"
                                                    stop-opacity="0.25"
                                                />
                                                <stop
                                                    offset="100%"
                                                    stop-color="#3B9B50"
                                                    stop-opacity="0"
                                                />
                                            </linearGradient>
                                        </defs>

                                        <path
                                            d="M0 45 C45 55 55 75 100 68 S165 85 200 78 S260 105 300 92 S360 110 400 100 S460 120 500 108 S555 125 600 112 L600 180 L0 180 Z"
                                            fill="url(#chartFill)"
                                        />

                                        <path
                                            d="M0 45 C45 55 55 75 100 68 S165 85 200 78 S260 105 300 92 S360 110 400 100 S460 120 500 108 S555 125 600 112"
                                            fill="none"
                                            stroke="#3B9B50"
                                            stroke-width="3"
                                            stroke-linecap="round"
                                        />
                                    </svg>

                                    <div class="chart-x-labels">
                                        <span>Week 1</span>
                                        <span>Week 2</span>
                                        <span>Week 3</span>
                                        <span>Week 4</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="dashboard-panel category-panel">
                            <div class="panel-heading">
                                <div>
                                    <h3>Waste by category</h3>
                                    <p>Illustrative category distribution</p>
                                </div>
                            </div>

                            <div class="category-bars">
                                {#each bars as bar}
                                    <div class="category-row">
                                        <div class="category-info">
                                            <span>{bar.name}</span>
                                            <strong>{bar.kg} kg</strong>
                                        </div>

                                        <div class="category-track">
                                            <div
                                                class="category-fill"
                                                style={`width: ${bar.value}%; background: ${bar.color}`}
                                            ></div>
                                        </div>
                                    </div>
                                {/each}
                            </div>

                            <div class="category-note">
                                <Info size={15} />
                                Sample values for interface demonstration.
                            </div>
                        </div>
                    </div>

                    <div class="dashboard-panel recent-panel">
                        <div class="panel-heading">
                            <div>
                                <h3>Recent predictions</h3>
                                <p>Your latest food waste estimates</p>
                            </div>

                            <button
                                class="text-button"
                                onclick={() => navigate('history')}
                            >
                                View all
                                <ArrowRight size={16} />
                            </button>
                        </div>

                        <div class="table-wrap">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Prediction ID</th>
                                        <th>Date</th>
                                        <th>Meals served</th>
                                        <th>Food category</th>
                                        <th>Predicted waste</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {#each historyRows as row}
                                        <tr>
                                            <td><strong>{row.id}</strong></td>
                                            <td>{row.date}</td>
                                            <td>{row.meals}</td>
                                            <td>
                                                <span class="category-pill">
                                                    {row.category}
                                                </span>
                                            </td>
                                            <td>
                                                <strong>{row.waste} kg</strong>
                                            </td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>

                        <p class="sample-disclaimer">
                            These are sample dashboard records, not saved predictions
                            from the backend.
                        </p>
                    </div>

                    <div class="impact-card">
                        <div class="impact-card-icon">
                            <Sprout size={25} />
                        </div>

                        <div>
                            <h3>Small changes create a bigger impact.</h3>
                            <p>
                                Predict demand, prepare smarter portions and
                                reduce avoidable food waste.
                            </p>
                        </div>

                        <button
                            class="impact-card-button"
                            onclick={() => navigate('prediction')}
                        >
                            Get started
                            <ArrowRight size={17} />
                        </button>
                    </div>
                </section>

            {:else if page === 'prediction'}

                <PredictionPage />

            {:else if page === 'analytics'}

                <AnalyticsPage />

            {:else if page === 'history'}
            
                <HistoryPage />

            {:else if page === 'about'}
                <AboutPage />

            {:else}

                <section class="page">
                    <div class="page-header">
                        <div>
                            <div class="eyebrow">FOODWISE AI WORKSPACE</div>
                            <h1>{navItems.find(item => item.id === page)?.label}</h1>
                            <p>
                                Explore this section of your food waste management
                                workspace.
                            </p>
                        </div>
                    </div>

                    <div class="dashboard-panel placeholder-panel">
                        <div class="placeholder-icon">
                            {#if page === 'history'}
                                <History size={30} />
                            {:else}
                                <Info size={30} />
                            {/if}
                        </div>

                        <h2>
                            {navItems.find(item => item.id === page)?.label}
                        </h2>

                        <p>We will implement this section next.</p>

                        <button
                            class="primary-button"
                            onclick={() => navigate('dashboard')}
                        >
                            <LayoutDashboard size={17} />
                            Back to dashboard
                        </button>
                    </div>
                </section>

            {/if}
        </main>
    </div>
</div>
