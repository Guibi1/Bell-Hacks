<script lang="ts">
    import { Avatar } from "@skeletonlabs/skeleton";

    export let data;
</script>

You made it!

<ul class="list">
    {#each data.passwords as password}
        <li>
            <Avatar src={`https://${password.website}.com/favicon.ico`} />
            <span class="flex-auto">{password.website}</span>
        </li>
    {/each}
</ul>
