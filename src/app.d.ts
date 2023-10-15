import type { User as U } from "$lib/schemas";

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
    namespace App {
        type User = U;
        // interface Error {}
        interface Locals {
            callId: string | null;
            userId: string | null;
        }
        interface PageData {
            isFr: boolean;
            lang: string;
            isLoggedIn: boolean;
        }
        // interface Platform {}
    }
}

export {};
