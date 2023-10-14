import { wordList } from "$lib/word-list";

export function generateUserId() {
    let id: string = "";

    for (let i = 0; i < 26; i++) {
        id += alphanumerics[Math.floor(Math.random() * alphanumerics.length)];
    }

    return id;
}

export function generatePrivateKey() {
    const words: string[] = [];

    for (let i = 0; i < 4; i++) {
        words.push(wordList[Math.floor(Math.random() * wordList.length)]);
    }

    return words;
}

const alphanumerics = "abcdefghijklmnopqrstuvwxyz1234567890";
