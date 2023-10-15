<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { getModalStore } from "@skeletonlabs/skeleton";
    import { api } from "sveltekit-typesafe-api";
    const modalStore = getModalStore();

    export let parent: any;

    let message = "";
    let phone = "";
    let key1 = "";
    let key2 = "";
    let key3 = "";
    let key4 = "";

    async function submit() {
        modalStore.close();
        const res = await api.POST("/login", {
            body: { phone, privateKey: [key1, key2, key3, key4] },
        });
        const json = await res.json();
        if (json.success) {
            goto(`/${$page.data.lang}/vault`);
        } else if (json.invalidPassword) {
            message = "Invalid password";
        } else {
            message = "";
        }
    }
</script>

{#if $modalStore[0]}
    <div class="modal-example-form card w-modal space-y-4 p-4 shadow-xl">
        <header class="text-2xl font-bold">
            {$page.url.pathname.startsWith("/fr") ? "Se connecter" : "Sign in"}
        </header>
        <article>
            {$page.url.pathname.startsWith("/fr")
                ? "Entrez vos mots secrets dans les boîtes ci-dessous"
                : "Put your secret keywords in the boxes below"}
        </article>

        <form class="modal-form space-y-4 border border-surface-500 p-4 rounded-container-token">
            {#if message}
                <span class="text-error-400-500-token">{message}</span>
            {/if}

            <label class="label">
                <span>
                    {$page.url.pathname.startsWith("/fr") ? "Numéro de téléphone" : "Phone number"}
                </span>
                <input class="input" type="tel" bind:value={phone} placeholder="Enter phone..." />
            </label>

            <label class="label">
                <span>
                    {$page.url.pathname.startsWith("/fr") ? "Mots secrets" : "Secret keywords"}
                </span>
                <div class="flex">
                    <input class="input" type="text" bind:value={key1} />
                    <input class="input" type="text" bind:value={key2} />
                    <input class="input" type="text" bind:value={key3} />
                    <input class="input" type="text" bind:value={key4} />
                </div>
            </label>
        </form>

        <footer class="modal-footer {parent.regionFooter}">
            <button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>
                {$page.url.pathname.startsWith("/fr") ? "Annuler" : "Cancel"}
            </button>
            <button class="btn {parent.buttonPositive}" on:click={submit}>
                {$page.url.pathname.startsWith("/fr") ? "Se connecter" : "Sign in"}
            </button>
        </footer>
    </div>
{/if}
