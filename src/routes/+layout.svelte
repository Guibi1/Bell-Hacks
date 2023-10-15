<script lang="ts">
    import { AppShell, AppBar,getModalStore, initializeStores, Modal  } from "@skeletonlabs/skeleton";
    import logoTitle from "$assets/PhoneBase-logo.png";
    import MyCustomComponent from "./connectionForm.svelte";
    

    initializeStores();
    const modalStore = getModalStore();

    const formData = {
        fourKeywords: "Jane Doe",
        tel: "214-555-1234",
        email: "jdoe@email.com",
    };

    function popUpForm() {
        modalStore.trigger({
            type: "component",
            component: { ref: MyCustomComponent },
        });
    }

    import "../app.postcss";
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
                <button class="variant-filled-primary btn" on:click={() => popUpForm()}
                    >Sign in<button> </button></button
                ></svelte:fragment
            >
        </AppBar>
    </svelte:fragment>
    

    <slot />
</AppShell>
