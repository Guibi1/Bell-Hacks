<script lang="ts">
    import { goto, invalidateAll } from "$app/navigation";
    import { page } from "$app/stores";
    import logoTitle from "$assets/PhoneBase-logo.png";
    import {
        AppBar,
        AppShell,
        LightSwitch,
        Modal,
        getModalStore,
        initializeStores,
    } from "@skeletonlabs/skeleton";
    import { api } from "sveltekit-typesafe-api";
    import "../../app.postcss";
    import ConnectionFormModal from "./ConnectionFormModal.svelte";

    initializeStores();
    const modalStore = getModalStore();

    async function openConnectModal() {
        if ($page.data.isLoggedIn) {
            if ($page.route.id?.endsWith("vault")) {
                await api.POST("/logout", {});
                invalidateAll();
                goto(`/${$page.data.lang}`);
            } else {
                goto(`/${$page.data.lang}/vault`);
            }
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
        <AppBar background="bg-secondary-500-400-token">
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
                <button class="variant-filled-tertiary btn" on:click={openConnectModal}>
                    {#if !$page.data.isLoggedIn}
                        {$page.data.isFr ? "Se connecter" : "Sign in"}
                    {:else if $page.route.id?.endsWith("vault")}
                        {$page.data.isFr ? "Se déconnecter" : "Log out"}
                    {:else}
                        {$page.data.isFr ? "Coffre-fort" : "Vault"}
                    {/if}
                </button>

                <LightSwitch />

                <a
                    class="variant-filled-tertiary btn btn-icon"
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
