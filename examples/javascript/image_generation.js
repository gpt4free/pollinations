/**
 * Example demonstrating image generation with various models and options.
 * 
 * This script shows how to generate images using different models, sizes,
 * and parameters.
 */

import { Pollinations } from '@gpt4free/g4f.dev';

async function main() {
  console.log('='.repeat(70));
  console.log('Image Generation Examples');
  console.log('='.repeat(70));
  
  // Initialize client
  const client = new Pollinations();
  
  // ========================================================================
  // Basic Image Generation
  // ========================================================================
  
  console.log('\n1. Simple Image Generation:');
  console.log('-'.repeat(70));
  const result1 = await client.images.generate({
    prompt: 'A beautiful sunset over mountains'
  });
  console.log(`Image URL: ${result1.data[0].url}`);
  
  console.log('\n2. Image with Specific Model (flux):');
  console.log('-'.repeat(70));
  const result2 = await client.images.generate({
    model: 'flux',
    prompt: 'A futuristic city skyline at night',
    size: '512x512'
  });
  console.log(`Image URL: ${result2.data[0].url}`);
  
  console.log('\n3. Image with Different Size:');
  console.log('-'.repeat(70));
  const result3 = await client.images.generate({
    prompt: 'A serene lake with mountains in the background',
    size: '1024x768'
  });
  console.log(`Image URL: ${result3.data[0].url.substring(0, 80)}...`);
  
  console.log('\n4. Image with SDXL Turbo Model:');
  console.log('-'.repeat(70));
  const result4 = await client.images.generate({
    model: 'sdxl-turbo',
    prompt: 'Abstract geometric patterns in vibrant colors',
    size: '512x512'
  });
  console.log(`Image URL: ${result4.data[0].url.substring(0, 80)}...`);
  
  console.log('\n5. Multiple Images (if supported):');
  console.log('-'.repeat(70));
  const result5 = await client.images.generate({
    prompt: 'A cute cat wearing sunglasses',
    size: '512x512',
    n: 1 // Number of images
  });
  console.log(`Generated ${result5.data.length} image(s)`);
  result5.data.forEach((img, idx) => {
    console.log(`Image ${idx + 1} URL: ${img.url.substring(0, 60)}...`);
  });
  
  // ========================================================================
  // Browser Usage Example (commented out for Node.js)
  // ========================================================================
  
  console.log('\n6. Browser Usage Example (see code):');
  console.log('-'.repeat(70));
  console.log('// For browser usage:');
  console.log(`
const result = await client.images.generate({
  model: 'flux',
  prompt: 'A futuristic city skyline at night',
  size: '512x512'
});

const image = new Image();
image.src = result.data[0].url;
document.body.appendChild(image);
  `);
  
  // ========================================================================
  // Accessing Response Properties
  // ========================================================================
  
  console.log('\n7. Accessing Response Properties:');
  console.log('-'.repeat(70));
  const result7 = await client.images.generate({
    prompt: 'A peaceful zen garden',
    model: 'flux'
  });
  console.log(`Created timestamp: ${result7.created}`);
  console.log(`Number of images: ${result7.data.length}`);
  console.log(`Image URL: ${result7.data[0].url.substring(0, 60)}...`);
  if (result7.data[0].revised_prompt) {
    console.log(`Revised Prompt: ${result7.data[0].revised_prompt}`);
  }
  
  console.log('\n' + '='.repeat(70));
  console.log('Image generation examples completed!');
  console.log('='.repeat(70));
}

// Run the examples
main().catch(console.error);
