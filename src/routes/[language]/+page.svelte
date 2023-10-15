<script lang="ts">
    import { page } from "$app/stores";
</script>

<main class="flex flex-col p-4">
    <a
        class="card variant-ghost-primary card-hover mx-auto flex flex-col self-center p-8 text-center"
        href="tel:+14388123367"
    >
        <span class="text-3xl">- {$page.data.isFr ? "Appelez Maintenant" : "Call Now"} -</span>
        <span class="text-5xl">(438) 812-3367</span>
    </a>

    <div class="div m-10">
        <h3 class="h3 text-center underline">
            {$page.data.isFr ? "À propos" : "About"}
        </h3>

        <p class="h5 p-4">
            {$page.data.isFr
                ? `Vos mots de passe sont incryptés avec notre algothime d'incryption Learning With Error;
            donnant à ceux-ci une sécurité quantique et 0% basée sur la confiance. De plus, notre
            service à la clientèle basée sur l'IA répondra à toutes vos questions sans soucis!`
                : `We are a unique password manager accessible through your phone! Your passwords are
            encrypted using our Learning With Error encryption algorithm; making it quantum-safe and
            0% trust-based and our AI-based customer service can help you with any password-related
            questions with no issues at all!`}
        </p>
    </div>

    <div class="grid grid-cols-4 self-center">
        <img class="h-40" src="src/assets/PhoneBase-logo.png" alt="1" />
        <img class="h-40" src="src/assets/PhoneBase-logo.png" alt="2" />
        <img class="h-40" src="src/assets/PhoneBase-logo.png" alt="3" />
        <img class="h-40" src="src/assets/PhoneBase-logo.png" alt="4" />
    </div>
</main>
