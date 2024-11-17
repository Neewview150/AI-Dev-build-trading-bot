export function calculateEMA(data, period) {
  const alpha = 2 / (period + 1);
  let ema = [data[0]];

  for (let i = 1; i < data.length; i++) {
    ema.push(data[i] * alpha + ema[i - 1] * (1 - alpha));
  }

  return ema;
}

export function calculateGChannel(data, length) {
  const src = data.map(candle => candle.close);
  const a = new Array(src.length).fill(0);
  const b = new Array(src.length).fill(0);
  
  for (let i = 1; i < src.length; i++) {
    a[i] = Math.max(src[i], a[i-1]) - (a[i-1] - b[i-1]) / length;
    b[i] = Math.min(src[i], b[i-1]) + (a[i-1] - b[i-1]) / length;
  }

  const avg = a.map((val, i) => (val + b[i]) / 2);
  const signals = [];

  for (let i = 1; i < src.length; i++) {
    if (b[i-1] < src[i-1] && b[i] > src[i]) {
      signals.push('buy');
    } else if (a[i-1] < src[i-1] && a[i] > src[i]) {
      signals.push('sell');
    } else {
      signals.push('hold');
    }
  }

  return { signals, avg };
}