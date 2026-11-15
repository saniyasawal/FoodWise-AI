
<script lang="ts">
    import '../app.css';
    import favicon from '#lib/assets/favicon.svg';
    import type { LayoutProps } from './$types';

    let { children }: LayoutProps = $props();
</script>

<svelte:head>
    <link rel="icon" href={favicon} />
    <title>FoodWise | Food Surplus & Spoilage Predictor</title>
    <meta
        name="description"
        content="Predict food waste and make smarter food management decisions."
    />
</svelte:head>

{@render children()}
