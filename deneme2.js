// JS equivalent of this CSS monstrosity

// const text = ["GO", "FOR", "IT"];
// const textContainer = document.getElementById("text-container");
// const colors = ["#468B97", "#EF6262", "#F3AA60", "#1D5B79"];

// const renderText = (textToRender) => {
//   textToRender.forEach((text, idx) => {
//     const divElem = document.createElement("div");
//     divElem.setAttribute("class", `${idx}-line`);
//     const h1Element = document.createElement("h1");
//     h1Element.textContent = text;
//     divElem.appendChild(h1Element);

//     addShadow(divElem, idx);
//     textContainer.appendChild(divElem);
//   });
// };

// const addShadow = (element, elementIdx) => {
//   const coloredTextShadow = [];
//   const blackShadow = [];
//   for (let i = 0; i < 500; i += 1) {
//     const elementColor = colors[elementIdx];
//     // How far left
//     const coloredShadowOffsetX = i * -1;
//     // How deep down
//     const coloredShadowOffsetY = i;
//     const str = `${coloredShadowOffsetX}px ${coloredShadowOffsetY}px ${elementColor}`;
//     coloredTextShadow.push(str);

//     // Adding similar patter for the shadow
//     const shadowOffsetY = i * 10;
//     if (shadowOffsetY < 500) {
//       const shadowOffsetX = (i + 1) * 10;
//       const shadowString = `-${shadowOffsetX}px ${shadowOffsetY}px 15px rgba(0,0,0,0.4)`;
//       blackShadow.push(shadowString);
//     }
//   }

//   const shadows = coloredTextShadow.concat(blackShadow);
//   element.style.textShadow = shadows.join(", ");
// };

// renderText(text);
