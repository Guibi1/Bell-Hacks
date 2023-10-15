<script lang="ts">
    import { page } from "$app/stores";
    import samuel from "$assets/samuel.png";
    import gabriel from "$assets/gabriel.png";
    import olivier from "$assets/olivier.png";
    import laurent from "$assets/laurent.png";
</script>

<main class="flex flex-col p-4">
    <a
        class="card variant-ghost-primary card-hover mx-auto flex flex-col self-center p-8 text-center"
        href="tel:+14388123367"
    >
        <span class="text-3xl">- {$page.data.isFr ? "Appelez Maintenant" : "Call Now"} -</span>
        <span class="text-5xl">(438) 812-3367</span>
    </a>

    <section class="m-10">
        <h3 class="h3 text-center underline">
            {$page.data.isFr ? "À propos" : "About"}
        </h3>

        <p class="h5 p-4">
            {$page.data.isFr
                ? `Nous sommes un gestionnaire de mots de passe unique accessible depuis votre téléphone ! Vos mots de passe sont cryptés à l'aide de notre algorithme de cryptage Learning With Error, ce qui le rend sûr sur le plan quantique et basé sur une confiance à 0 %. Notre service client basé sur l'IA peut vous aider pour toute question relative aux mots de passe sans aucun problème !`
                : `We are a unique password manager accessible through your phone! Your passwords are encrypted using our Learning With Error encryption algorithm, making it quantum-safe and 0% trust-based. Our AI-based customer service can assist you with any password-related questions without any issues at all!`}
        </p>
    </section>

    <section class="flex flex-col gap-8 pb-4">
        <h3 class="h3 text-center underline">
            {$page.data.isFr ? "L'équipe" : "The team"}
        </h3>

        <div
            class="grid grid-cols-2 gap-8 self-center px-8 md:w-5/6 lg:w-3/5 xl:w-3/4 xl:grid-cols-4 2xl:w-8/12"
        >
            <a
                class="card variant-filled-primary card-hover overflow-hidden text-center"
                href="https://www.instagram.com/lyddeon/"
            >
                <img class="w-full" src={samuel} alt="Samuel" />

                <div class="p-4">
                    <span class="text-3xl">Samuel</span>

                    <p class="p text-xl">Creative lead</p>
                </div>
            </a>

            <a
                class="card variant-filled-primary card-hover overflow-hidden text-center"
                href="https://www.linkedin.com/in/gabriel-mikus-728a2326b/"
            >
                <img class="w-full" src={gabriel} alt="Gabriel" />

                <div class="p-4">
                    <span class="text-3xl">Gabriel</span>

                    <p class="p text-xl">Prompt engineer</p>
                </div>
            </a>

            <a
                class="card variant-filled-primary card-hover overflow-hidden text-center"
                href="https://www.linkedin.com/in/olivier-saint-vincent/"
            >
                <img class="w-full" src={olivier} alt="Olivier" />

                <div class="p-4">
                    <span class="text-3xl">Olivier</span>

                    <p class="p text-xl">Number theorist</p>
                </div>
            </a>

            <a
                class="card variant-filled-primary card-hover overflow-hidden text-center"
                href="https://www.linkedin.com/in/guibi1/"
            >
                <img class="w-full" src={laurent} alt="Laurent" />

                <div class="flex flex-col p-4">
                    <span class="text-3xl">Laurent</span>

                    <p class="p text-xl">Full-Stack dev</p>
                </div>
            </a>
        </div>
    </section>
</main>
