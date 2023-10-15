<script lang="ts">
    import { AppShell, AppBar } from "@skeletonlabs/skeleton";
    import logoTitle from "$assets/PhoneBase-logo.png";

    import "../app.postcss";
</script>

<AppShell>
    <svelte:fragment slot="header">
        <AppBar background="bg-surface-500">
            <svelte:fragment slot="lead">
                <img class="h-20" src={logoTitle} alt="logo" />
            </svelte:fragment>

            <h1 class="h1">PhoneBase</h1>
            <h2 class="h4">Quantum-Secured Password Manager</h2>

            <svelte:fragment slot="trail">
                <a  class="btn variant-filled-primary" >Sign in</a> 
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>

    <slot />
</AppShell>
