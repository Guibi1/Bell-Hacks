import { sveltekit } from "@sveltejs/kit/vite";
import { typesafeApi } from "sveltekit-typesafe-api/vite";
import { defineConfig } from "vite";

export default defineConfig({
    plugins: [sveltekit(), typesafeApi()],
    server: {
        fs: { allow: ["api"] },
    },
});
