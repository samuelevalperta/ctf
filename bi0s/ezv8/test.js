// Simple V8 test script

// Function to test basic arithmetic
function testArithmetic() {
  console.log("Arithmetic Test:");

  // Addition
  console.log("1 + 1 =", 1 + 1);

  // Subtraction
  console.log("5 - 3 =", 5 - 3);

  // Multiplication
  console.log("4 * 6 =", 4 * 6);

  // Division
  console.log("10 / 2 =", 10 / 2);

  // Modulus
  console.log("7 % 3 =", 7 % 3);
}

// Function to test arrays
function testArrays() {
  console.log("\nArrays Test:");

  // Creating an array
  const fruits = ["apple", "banana", "orange"];

  // Accessing elements
  console.log("First fruit:", fruits[0]);
  console.log("Number of fruits:", fruits.length);

  // Adding an element
  fruits.push("grape");
  console.log("Fruits after adding 'grape':", fruits);
}

// Function to test asynchronous code
async function testAsync() {
  console.log("\nAsynchronous Test:");

  // Using a Promise
  const promise = new Promise((resolve) => {
    setTimeout(() => {
      resolve("Async operation complete");
    }, 2000);
  });

  const result = await promise;
  console.log(result);
}

// Run the tests
testArithmetic();
testArrays();
testAsync();

