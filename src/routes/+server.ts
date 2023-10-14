import { decrypt, encrypt, generateKeyPairs, verifyPrivateKey } from "$lib/crypto";
import { json } from "@sveltejs/kit";

export async function GET({ fetch }) {
    const { publicKey, privateKey } = await generateKeyPairs(fetch);
    console.log("🚀 ~ file: +server.ts:6 ~ GET ~ publicKey:", publicKey);
    console.log("🚀 ~ file: +server.ts:6 ~ GET ~ privateKey:", privateKey);

    const verifyGood = await verifyPrivateKey(fetch, privateKey, publicKey);
    console.log("🚀 ~ file: +server.ts:10 ~ GET ~ verifyGood:", verifyGood);

    const encrypted = await encrypt(fetch, publicKey, "PASSWORD1234");
    console.log("🚀 ~ file: +server.ts:13 ~ GET ~ encrypted:", encrypted);
    const decrypted = await decrypt(fetch, privateKey, publicKey, encrypted);
    console.log("🚀 ~ file: +server.ts:15 ~ GET ~ decrypted:", decrypted);

    return json({ verifyGood, encrypted, decrypted });
}
