import adapter from "@sveltejs/adapter-auto";
import type { Config } from "@sveltejs/kit";
import { vitePreprocess } from "@sveltejs/kit/vite";

const config: Config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter(),
        csrf: { checkOrigin: false },
    },
};

export default config;
