import * as fs from 'fs';

// Function to load words from a file
function loadWordsFromFile(filename: string): string[] {
  const words: string[] = fs.readFileSync(filename, 'utf-8').split('\n').map(word => word.trim());
  return words;
}

// Function to generate a random password
function generateRandomPassword(
  wordList: string[],
  minWords: number,
  maxWords: number,
  minNumbers: number,
  maxNumbers: number,
  minChars: number,
  maxChars: number
): string {
  const numWords: number = getRandomInt(minWords, maxWords);
  const numNumbers: number = getRandomInt(minNumbers, maxNumbers);
  const numChars: number = getRandomInt(minChars, maxChars);

  const selectedWords: string[] = getRandomElements(wordList, numWords);
  const selectedNumbers: string = getRandomNumbers(numNumbers);
  const selectedChars: string = getRandomCharacters(numChars);


  for (let i: number = 0; i < selectedWords.length; i++) {
    if (Math.random() < 0.5) {
      selectedWords[i] = selectedWords[i][0].toUpperCase() + selectedWords[i].substring(1);
    }
  }

  const passwordParts: string[] = [...selectedWords, selectedNumbers, selectedChars];
  shuffleArray(passwordParts);

  return passwordParts.join('');
}

// Function to get a random integer between min and max (inclusive)
function getRandomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Function to get a random subset of elements from an array
function getRandomElements(array: string[], count: number): string[] {
  const shuffled: string[] = array.slice();
  shuffleArray(shuffled);
  return shuffled.slice(0, count);
}

// Function to shuffle an array in place
function shuffleArray(array: string[]): void {
  for (let i: number = array.length - 1; i > 0; i--) {
    const j: number = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// Function to generate random numbers
function getRandomNumbers(count: number): string {
  let result: string = '';
  for (let i: number = 0; i < count; i++) {
    result += String(Math.floor(Math.random() * 10));
  }
  return result;
}

// Function to generate random characters
function getRandomCharacters(count: number): string {
  const characters: string = "!@#$*,.?";
  let result: string = '';
  for (let i: number = 0; i < count; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

const wordList: string[] = loadWordsFromFile('LearningWithErrorsEncryption/words2000.txt');

export default async function generatePassword(){
  const password: string = generateRandomPassword(wordList, 1, 3, 3, 5, 3, 5);
  return password;
}
