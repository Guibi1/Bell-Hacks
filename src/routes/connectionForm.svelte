<script lang="ts">
    // Props
    /** Exposes parent props to this component. */
    export let parent: any;

    // Stores
    import { getModalStore } from "@skeletonlabs/skeleton";
    const modalStore = getModalStore();

    // We've created a custom submit function to pass the response and close the modal.
    function onFormSubmit(): void {
        modalStore.close();
    }

    // Base Classes
    const cBase = "card p-4 w-modal shadow-xl space-y-4";
    const cHeader = "text-2xl font-bold";
    const cForm = "border border-surface-500 p-4 space-y-4 rounded-container-token";
</script>

{#if $modalStore[0]}
    <div class="modal-example-form {cBase}">
        <header class={cHeader}>{$modalStore[0].title ?? "Sign In"}</header>
        <article>{$modalStore[0].body ?? "Put your secret keywords in the boxes below"}</article>

        <label class="label">
            <span>Phone Number</span>
            <input class="input" type="tel" placeholder="Enter phone..." />
        </label>
        <form class="modal-form {cForm}">
            <label class="label">
                <span>Keys</span>
                <div class="flex">
                    <input class="input" type="text" />
                    <input class="input" type="text" />
                    <input class="input" type="text" />
                    <input class="input" type="text" />
                </div>
            </label>
        </form>
        <!-- prettier-ignore -->
        <footer class="modal-footer {parent.regionFooter}">
        <button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
        <button class="btn {parent.buttonPositive}" on:click={onFormSubmit}>Submit Form</button>
    </footer>
    </div>
{/if}
