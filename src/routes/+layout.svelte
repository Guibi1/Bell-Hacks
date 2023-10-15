<script lang="ts">
    import logoTitle from "$assets/PhoneBase-logo.png";
    import {
        AppBar,
        AppShell,
        Modal,
        getModalStore,
        initializeStores,
    } from "@skeletonlabs/skeleton";
    import "../app.postcss";
    import ConnectionFormModal from "./ConnectionFormModal.svelte";
    import { page } from "$app/stores";

    initializeStores();
    const modalStore = getModalStore();

    export let data;

    function popUpForm() {
        modalStore.trigger({
            type: "component",
            component: {
                ref: ConnectionFormModal,
                props: { data: data.form },
            },
        });
    }
</script>

<Modal></Modal>
<AppShell>
    <svelte:fragment slot="header">
        <AppBar background="bg-surface-500">
            <svelte:fragment slot="lead">
                <img class="h-20" src={logoTitle} alt="logo" />
            </svelte:fragment>

            <h1 class="h1">PhoneBase</h1>
            <h2 class="h4">Quantum-Secured Password Manager</h2>

            <svelte:fragment slot="trail">
                <a class="" href={$page.url.pathname.startsWith("/fr") ? "/" : "/fr"}>
                    {$page.url.pathname.startsWith("/fr") ? "En" : "Fr"}
                </a>

                <button class="variant-filled-primary btn" on:click={popUpForm}> 
                    {$page.url.pathname.startsWith("/fr") ? "Se connecter" : "Sign in"}</button>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>

    <slot />
</AppShell>
