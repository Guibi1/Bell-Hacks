<script lang="ts">
    import logoTitle from "$assets/PhoneBase-logo.png";
    import {
        AppBar,
        AppShell,
        LightSwitch,
        Modal,
        getModalStore,
        initializeStores,
    } from "@skeletonlabs/skeleton";
    import "../app.postcss";
    import ConnectionFormModal from "./ConnectionFormModal.svelte";

    initializeStores();
    const modalStore = getModalStore();

    function openConnectModal() {
        modalStore.trigger({
            type: "component",
            component: {
                ref: ConnectionFormModal,
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
                <a class="" href="/fr"> Fr </a>

                <LightSwitch />

                <button class="variant-filled-primary btn" on:click={openConnectModal}>
                    Sign in
                </button>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>

    <slot />
</AppShell>
