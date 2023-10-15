<script lang="ts">
    import { Avatar } from "@skeletonlabs/skeleton";

    export let data;
</script>

You made it!

<ul class="list">
    {#each data.passwords as password}
        <li>
            <div class="aspect-square h-12 overflow-hidden">
                <img src={`https://${password.website}.com/favicon.ico`} alt="website favicon" />
            </div>
            <span class="flex-auto">{password.website}</span>
        </li>
    {/each}
</ul>
