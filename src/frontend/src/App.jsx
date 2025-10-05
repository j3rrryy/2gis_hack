import React, { useEffect, useRef, useState } from 'react';
import { createCalculation, pollCalculation, fetchAddress } from './api.js';

// MapGL API key (2GIS) fixed per user instruction
const MAP_KEY = '285d3b2b-96ab-4fe5-a700-12ef370d7085';

/**
 * Compute the top three features from the result object based on the overall score.
 * If score >= 70 (7/10), choose the top three highest values (best features) and color green.
 * If 40 <= score < 70 (4-6/10), choose the middle three values and color orange.
 * Otherwise, choose the three lowest values and color red.
 *
 * @param {Object} result Result object returned from the backend containing score and feature values
 * @returns {{features: Array<{key: string, value: number}>, color: string}}
 */
function computeTopFeatures(result) {
  const { score, ...others } = result || {};
  const entries = Object.entries(others).filter(
    ([k, v]) => typeof v === 'number' && !Number.isNaN(v)
  );
  const n = entries.length;
  if (n === 0) {
    return { features: [], color: 'feature-green' };
  }
  // Determine color and ordering based on score threshold
  let color;
  let sorted;
  if (score >= 7) {
    // High rating: pick top three highest values and color green
    color = 'feature-green';
    sorted = entries.sort((a, b) => b[1] - a[1]);
    return {
      color,
      features: sorted.slice(0, Math.min(3, n)).map(([key, value]) => ({ key, value })),
    };
  } else if (score >= 4) {
    // Mid rating: pick three middle values and color orange
    color = 'feature-orange';
    sorted = entries.sort((a, b) => a[1] - b[1]);
    if (n <= 3) {
      return {
        color,
        features: sorted.map(([key, value]) => ({ key, value })),
      };
    }
    const start = Math.floor((n - 3) / 2);
    return {
      color,
      features: sorted.slice(start, start + 3).map(([key, value]) => ({ key, value })),
    };
  } else {
    // Low rating: pick three lowest values and color red
    color = 'feature-red';
    sorted = entries.sort((a, b) => a[1] - b[1]);
    return {
      color,
      features: sorted.slice(0, Math.min(3, n)).map(([key, value]) => ({ key, value })),
    };
  }
}

/**
 * Format a feature key into a more human-friendly label.
 * Converts underscores to spaces and capitalises the first letter.
 *
 * @param {string} key
 * @returns {string}
 */
function formatFeatureKey(key) {
  if (!key) return '';
  const withSpaces = key.replace(/_/g, ' ');
  return withSpaces.charAt(0).toUpperCase() + withSpaces.slice(1);
}

/**
 * Render the score as individual digit spans. Each digit will use the IBM Plex Serif
 * font via the CSS class "digit" defined in styles.css.
 *
 * @param {number} score
 * @returns {JSX.Element[]}
 */
function renderScoreDigits(score) {
  const str = String(Math.round(score || 0));
  return str.split('').map((ch, idx) => (
    <span key={idx} className="digit">
      {ch}
    </span>
  ));
}

export default function App() {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const markerRef = useRef(null);

  const [resultData, setResultData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mapLoaded, setMapLoaded] = useState(false);

  // Загружаем скрипт 2GIS
  useEffect(() => {
    if (window.mapgl) {
      setMapLoaded(true);
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://mapgl.2gis.com/api/js/v1';
    script.async = true;
    script.onload = () => setMapLoaded(true);
    script.onerror = () => console.error('Failed to load 2GIS map script');
    document.head.appendChild(script);

    return () => {
      if (script.parentNode) {
        script.parentNode.removeChild(script);
      }
    };
  }, []);

  // Инициализируем карту после загрузки скрипта
  useEffect(() => {
    if (!mapLoaded || !mapContainerRef.current) return;

    let isMounted = true;

    try {
      const map = new window.mapgl.Map(mapContainerRef.current, {
        center: [37.617635, 55.755814],
        zoom: 12,
        key: MAP_KEY,
      });

      mapRef.current = map;

      // Click handler: send calculation and update UI
      map.on('click', async (event) => {
        const lon = event.lngLat[0];
        const lat = event.lngLat[1];

        // Place marker
        if (markerRef.current) {
          markerRef.current.destroy();
        }
        markerRef.current = new window.mapgl.Marker(map, {
          coordinates: [lon, lat],
        });

        setLoading(true);
        try {
          // Fetch address
          const address = await fetchAddress(lat, lon, MAP_KEY);
          // Start calculation (проверь порядок координат в API!)
          const calcId = await createCalculation(lon, lat); // Обычно X=lon, Y=lat
          const result = await pollCalculation(calcId);
          // Compute top features and color
          const { features, color } = computeTopFeatures(result);
          if (isMounted) {
            setResultData({
              score: result.score,
              address,
              features,
              color,
            });
          }
        } catch (err) {
          console.error('Error:', err);
        } finally {
          if (isMounted) setLoading(false);
        }
      });

    } catch (error) {
      console.error('Map initialization error:', error);
    }

    return () => {
      isMounted = false;
      if (mapRef.current) {
        mapRef.current.destroy();
        mapRef.current = null;
      }
    };
  }, [mapLoaded]);

  return (
    <div className="app-container">
      <div className="map-container" ref={mapContainerRef}></div>
      {!mapLoaded && (
        <div className="result-card">
          <div className="score">Загрузка карты…</div>
        </div>
      )}
      {resultData && !loading && (
        <div className="result-card">
          {/* Big score number */}
          <div className="score">{renderScoreDigits(resultData.score)}</div>
          {/* Features list */}
          {resultData.features.length > 0 && (
            <ul className="feature-list">
              {resultData.features.map((feature) => (
                <li key={feature.key} className={resultData.color}>
                  <span className="key">{formatFeatureKey(feature.key)}</span>
                  <span className="value">{feature.value}</span>
                </li>
              ))}
            </ul>
          )}
          {/* Address */}
          {resultData.address && <div className="address">{resultData.address}</div>}
        </div>
      )}
      {loading && (
        <div className="result-card">
          <div className="score">Загрузка…</div>
        </div>
      )}
    </div>
  );
}