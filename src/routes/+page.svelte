<script lang="ts">
    import { AppShell,AppBar } from '@skeletonlabs/skeleton';
	import logoTitle from "$assets/PhoneBase-Logo.png";
</script>





<AppBar  class="border-8">
	<svelte:fragment slot="lead">

		<img class="h-20" src={logoTitle} alt="logo">
	</svelte:fragment>
	<svelte:fragment slot="headline">

		<h1 class="h1">PhoneBase<h1>
		<h2 class="h4">Quantum-Secured Password Manager<h2>
	</svelte:fragment>

	
	
</AppBar>
	