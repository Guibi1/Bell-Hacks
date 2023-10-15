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
    import "../../app.postcss";
    import ConnectionFormModal from "./ConnectionFormModal.svelte";
    import { page } from "$app/stores";
    import { api } from "sveltekit-typesafe-api";
    import { invalidate } from "$app/navigation";

    initializeStores();
    const modalStore = getModalStore();

    async function openConnectModal() {
        if ($page.data.isLoggedIn) {
            await api.POST("/logout", {});
            invalidate("app:auth");
        } else {
            modalStore.trigger({
                type: "component",
                component: {
                    ref: ConnectionFormModal,
                },
            });
        }
    }
</script>

<Modal />

<AppShell>
    <svelte:fragment slot="header">
        <AppBar background="bg-surface-500">
            <svelte:fragment slot="lead">
                <img class="h-20" src={logoTitle} alt="logo" />
            </svelte:fragment>

            <h1 class="h1">PhoneBase</h1>
            <h2 class="h4">
                {$page.data.isFr
                    ? "Gestionnaire de mot de passe Quantique"
                    : "Quantum-Secured Password Manager"}
            </h2>

            <svelte:fragment slot="trail">
                <button class="variant-filled-primary btn" on:click={openConnectModal}>
                    {#if $page.data.isLoggedIn}
                        {$page.data.isFr ? "Se déconnecter" : "Log out"}
                    {:else}
                        {$page.data.isFr ? "Se connecter" : "Sign in"}
                    {/if}
                </button>

                <LightSwitch />

                <a
                    class="variant-filled-primary btn btn-icon"
                    href={$page.data.isFr
                        ? "/en" + $page.url.pathname.substring(3)
                        : "/fr" + $page.url.pathname.substring(3)}
                >
                    {$page.data.isFr ? "En" : "Fr"}
                </a>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>

    <slot />
</AppShell>
