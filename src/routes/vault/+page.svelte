<script lang="ts">
    import type { Password } from "$lib/schemas";
    import { Accordion, AccordionItem, Avatar, getModalStore } from "@skeletonlabs/skeleton";
    import { api } from "sveltekit-typesafe-api";

    export let data;
    let modalStore = getModalStore();
    let clearPassword: Record<number, string> = {};

    async function show(password: Password) {
        const res = await api.POST("/vault", { body: { id: password.id } });
        const { success, password: passwd } = await res.json();
        if (success) {
            clearPassword[password.id] = passwd;
        }
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
                await api.PUT("/vault", { body: { id: password.id, password: r } });
            },
        });
    }

    async function remove(password: Password) {
        data.passwords = data.passwords.filter((p) => p.id !== password.id);
        delete clearPassword[password.id];
        await api.DELETE("/vault", { body: { id: password.id } });
    }
</script>

You made it!
<main class="2xl:1/2 card mx-auto w-11/12 xl:w-8/12 2xl:w-1/2">
    <Accordion autocollapse>
        {#each data.passwords as password}
            <AccordionItem>
                <svelte:fragment slot="lead">
                    <Avatar src={`https://${password.website}.com/favicon.ico`} width="w-10" />
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <span class="flex-auto">{password.website}</span>
                </svelte:fragment>
                <div class="flex justify-between gap-8 p-4" slot="content">
                    <span>{clearPassword[password.id] ?? "**********"}</span>

                    <div class="flex gap-2">
                        <button class="variant-filled-primary btn" on:click={() => show(password)}>
                            Afficher
                        </button>
                        <button
                            class="variant-filled-primary btn"
                            on:click={() => modify(password)}
                        >
                            Modifier
                        </button>
                        <button class="variant-filled-error btn" on:click={() => remove(password)}>
                            Supprimer
                        </button>
                    </div>
                </div>
            </AccordionItem>
        {/each}
    </Accordion>
</main>
