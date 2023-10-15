<script lang="ts">
    import { goto, invalidateAll } from "$app/navigation";
    import { page } from "$app/stores";
    import { getModalStore } from "@skeletonlabs/skeleton";
    import { api } from "sveltekit-typesafe-api";
    const modalStore = getModalStore();

    export let parent: any;

    let website = "";
    let password = "";

    async function submit() {
        modalStore.close();
        await api.POST("/[language]/vault", {
            body: { website, password },
            routeParams: { language: $page.data.lang },
        });
        invalidateAll();
    }
</script>

{#if $modalStore[0]}
    <div class="modal-example-form card w-modal space-y-4 p-4 shadow-xl">
        <header class="text-2xl font-bold">
            {$page.url.pathname.startsWith("/fr")
                ? "Ajouter un mot de passe"
                : "Add a new password"}
        </header>
        <article>
            {$page.url.pathname.startsWith("/fr")
                ? "Entrez vos informations dans les boîtes ci-dessous"
                : "Put your information in the boxes below"}
        </article>

        <form
            class="modal-form space-y-4 border border-surface-500 p-4 rounded-container-token"
            on:submit={submit}
        >
            <label class="label">
                <span>
                    {$page.url.pathname.startsWith("/fr") ? "Nom du site web" : "Website name"}
                </span>
                <input
                    class="input"
                    type="text"
                    bind:value={website}
                    placeholder="Google"
                    required={true}
                />
            </label>

            <label class="label">
                <span>
                    {$page.url.pathname.startsWith("/fr") ? "Mot de passe" : "Password"}
                </span>
                <input
                    class="input"
                    type="password"
                    minlength="3"
                    maxlength="128"
                    required={true}
                    bind:value={password}
                />
            </label>
        </form>

        <footer class="modal-footer {parent.regionFooter}">
            <button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>
                {$page.url.pathname.startsWith("/fr") ? "Annuler" : "Cancel"}
            </button>
            <button class="btn {parent.buttonPositive}" on:click={submit}>
                {$page.url.pathname.startsWith("/fr") ? "Ajouter" : "Add"}
            </button>
        </footer>
    </div>
{/if}
