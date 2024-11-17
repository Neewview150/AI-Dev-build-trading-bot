import ccxt from 'ccxt';
import { config } from './config.js';

export function initializeExchange() {
  return new ccxt.binance({
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
}