import ccxt from 'ccxt';
import { config } from './config.js';

function retryWithExponentialBackoff(fn, retries = 5, delay = 1000) {
  return new Promise((resolve, reject) => {
    fn()
      .then(resolve)
      .catch((error) => {
        if (retries > 0 && error instanceof ccxt.RateLimitExceeded) {
          setTimeout(() => {
            retryWithExponentialBackoff(fn, retries - 1, delay * 2).then(resolve).catch(reject);
          }, delay);
        } else {
          reject(error);
        }
      });
  });
}

export function initializeExchange() {
  const exchange = new ccxt.binance({
    apiKey: config.apiKey,
    secret: config.apiSecret,
    enableRateLimit: true,
    options: {
      defaultType: 'spot',
      adjustForTimeDifference: true,
    },
    urls: {
      api: {
        spot: 'https://testnet.binance.vision/api/api/v3/ticker/24hr',
      },
    },
  });

  exchange.fetchTicker = (symbol) => {
    return retryWithExponentialBackoff(() => exchange.fetchTicker(symbol));
  };

  return exchange;
}