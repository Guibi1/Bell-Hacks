<script lang="ts">
    import { page } from "$app/stores";
    import type { Password } from "$lib/schemas";
    import {
        Accordion,
        AccordionItem,
        Avatar,
        ProgressRadial,
        getModalStore,
    } from "@skeletonlabs/skeleton";
    import { api } from "sveltekit-typesafe-api";

    export let data;
    let modalStore = getModalStore();
    let clearPassword: Record<number, Promise<string> | undefined> = {};

    async function show(password: Password) {
        clearPassword[password.id] = (
            await api
                .POST("/[language]/vault", {
                    body: { id: password.id },
                    routeParams: { language: $page.data.lang },
                })
                .then((res) => res.json())
        ).password;
    }

    async function modify(password: Password) {
        modalStore.trigger({
            type: "prompt",
            title: "Enter new password",
            body: `Provide the new password for ${password.website} in the field below.`,
            value: "",
            valueAttr: { type: "password", minlength: 3, maxlength: 128, required: true },
            response: async (r: string) => {
                delete clearPassword[password.id];
                clearPassword = clearPassword;
                await api.PUT("/[language]/vault", {
                    body: { id: password.id, password: r },
                    routeParams: { language: $page.data.lang },
                });
            },
        });
    }

    async function remove(password: Password) {
        data.passwords = data.passwords.filter((p) => p.id !== password.id);
        delete clearPassword[password.id];
        clearPassword = clearPassword;
        await api.DELETE("/[language]/vault", {
            body: { id: password.id },
            routeParams: { language: $page.data.lang },
        });
    }
</script>

<main class="2xl:1/2 card mx-auto my-8 w-11/12 xl:w-8/12 2xl:w-1/2">
    <Accordion autocollapse>
        {#each data.passwords as password}
            <AccordionItem>
                <svelte:fragment slot="lead">
                    <Avatar src={`https://${password.website}.com/favicon.ico`} width="w-10" />
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <span class="flex-auto">{password.website}</span>
                </svelte:fragment>

                <div
                    class="flex flex-col justify-stretch gap-2 p-4 align-middle md:flex-row"
                    slot="content"
                >
                    <div class="flex flex-1 items-center justify-center">
                        {#if clearPassword[password.id]}
                            {#await clearPassword[password.id]}
                                <ProgressRadial width="w-8" />
                            {:then password}
                                <pre
                                    class="pre w-full px-2 py-2 text-center md:w-auto md:px-12 lg:px-20">{password}</pre>
                            {/await}
                        {:else}
                            <pre
                                class="pre w-full px-2 py-2 text-center md:w-auto md:px-12 lg:px-20">**********</pre>
                        {/if}
                    </div>

                    <button class="variant-filled-primary btn" on:click={() => show(password)}>
                        {$page.data.isFr ? "Afficher" : "Show"}
                    </button>
                    <button class="variant-filled-primary btn" on:click={() => modify(password)}>
                        {$page.data.isFr ? "Modifier" : "Edit"}
                    </button>
                    <button class="variant-filled-error btn" on:click={() => remove(password)}>
                        {$page.data.isFr ? "Supprimer" : "Delete"}
                    </button>
                </div>
            </AccordionItem>
        {/each}
    </Accordion>
</main>
