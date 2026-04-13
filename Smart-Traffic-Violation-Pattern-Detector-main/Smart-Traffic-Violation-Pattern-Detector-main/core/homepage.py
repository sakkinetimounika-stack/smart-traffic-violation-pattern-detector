from __future__ import annotations

import streamlit as st


import streamlit.components.v1 as components

def inject_theme_tracker() -> None:
    components.html("""
    <script>
    function updateTheme() {
        try {
            var body = window.parent.document.body;
            var bgColor = window.parent.getComputedStyle(body).backgroundColor || window.parent.getComputedStyle(window.parent.document.documentElement).backgroundColor;
            var rgb = bgColor.match(/\\d+/g);
            if (rgb && rgb.length >= 3) {
                var brightness = (parseInt(rgb[0]) * 299 + parseInt(rgb[1]) * 587 + parseInt(rgb[2]) * 114) / 1000;
                if (brightness < 128) {
                    body.setAttribute('st-theme-mode', 'dark');
                } else {
                    body.setAttribute('st-theme-mode', 'light');
                }
            }
        } catch(e) {}
    }
    updateTheme();
    var observer = new MutationObserver(updateTheme);
    observer.observe(window.parent.document.body, { attributes: true, attributeFilter: ['style', 'class'] });
    var htmlObserver = new MutationObserver(updateTheme);
    htmlObserver.observe(window.parent.document.documentElement, { attributes: true, attributeFilter: ['style', 'class', 'data-theme'] });
    // Also periodically check just in case
    setInterval(updateTheme, 500);
    </script>
    """, height=0, width=0)

def inject_homepage_styles() -> None:
    inject_theme_tracker()
    st.markdown(
        """
        <style>
        .home-hero {
            text-align: center;
            background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 34%, #ede9fe 68%, #fef3c7 100%);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 28px;
            padding: 2.45rem 1.8rem 2.3rem 1.8rem;
            box-shadow: 0 20px 44px rgba(0, 0, 0, 0.10);
            margin-bottom: 1.35rem;
            position: relative;
            overflow: hidden;
        }
        .home-hero::before {
            content: ""; position: absolute; inset: 0;
            background: radial-gradient(circle at top right, rgba(255, 255, 255, 0.55), transparent 34%); pointer-events: none;
        }
        .home-hero-head { display: inline-flex; align-items: center; justify-content: center; gap: 0.9rem; margin-bottom: 1rem; position: relative; z-index: 1; }
        .home-hero-icon {
            width: 62px; height: 62px; border-radius: 18px; display: inline-flex; align-items: center; justify-content: center;
            font-size: 2rem; background: rgba(255, 255, 255, 0.78); box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12); flex-shrink: 0;
        }
        .home-hero-title { font-size: 2.65rem; font-weight: 800; line-height: 1.18; color: var(--text-color); margin: 0; }
        .home-hero-copy { max-width: 52rem; margin: 0 auto; font-size: 1.08rem; color: var(--text-color); opacity: 0.85; line-height: 1.72; position: relative; z-index: 1; }
        .home-divider { border: none; border-top: 1px solid rgba(128, 128, 128, 0.2); margin: 1.85rem 0 1.9rem 0; }
        .section-heading { display: flex; align-items: center; gap: 0.7rem; font-size: 1.95rem; font-weight: 800; color: var(--text-color); margin-bottom: 1rem; }
        .section-heading .emoji { font-size: 2rem; }
        .feature-visual-card {
            background: linear-gradient(145deg, #e0f2fe 0%, #dbeafe 35%, #ede9fe 100%);
            border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 22px; padding: 1.35rem; box-shadow: 0 16px 34px rgba(0, 0, 0, 0.06);
        }
        .feature-visual-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.9rem; margin-top: 1rem; }
        .feature-mini-tile {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 18px; padding: 1rem 0.9rem;
        }
        .feature-mini-tile strong { display: block; margin-bottom: 0.25rem; color: var(--text-color); }
        .feature-list-panel {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 22px; padding: 1.3rem 1.45rem; box-shadow: 0 16px 34px rgba(0, 0, 0, 0.06);
        }
        .feature-list-item { display: flex; gap: 0.8rem; align-items: flex-start; margin-bottom: 1.1rem; color: var(--text-color); }
        .feature-list-item:last-child { margin-bottom: 0; }
        .feature-bullet {
            width: 40px; height: 40px; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center;
            font-size: 1.1rem; line-height: 1; color: var(--primary-color) !important; background: color-mix(in srgb, var(--primary-color) 20%, transparent); flex-shrink: 0;
        }
        .feature-list-item strong { display: block; color: var(--text-color); font-size: 1.05rem; margin-bottom: 0.2rem; }
        .feature-list-item span { color: var(--text-color); opacity: 0.85; line-height: 1.55; }
        
        [st-theme-mode="dark"] .home-hero {
            background: #000000 !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
        }
        [st-theme-mode="dark"] .home-hero::before { background: none !important; }
        [st-theme-mode="dark"] .home-hero-icon { background: rgba(255, 255, 255, 0.1) !important; color: #ffffff !important; }
        
        [st-theme-mode="dark"] .feature-visual-card,
        [st-theme-mode="dark"] .feature-list-panel {
            background: #000000 !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
        }
        [st-theme-mode="dark"] .feature-mini-tile {
            background: #0a0a0a !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
        }
        
        /* Force pure white text in dark mode for absolute contrast */
        [st-theme-mode="dark"] .home-hero-title,
        [st-theme-mode="dark"] .home-hero-copy,
        [st-theme-mode="dark"] .feature-mini-tile strong,
        [st-theme-mode="dark"] .feature-list-item strong,
        [st-theme-mode="dark"] .feature-list-item span,
        [st-theme-mode="dark"] .section-heading,
        [st-theme-mode="dark"] div {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        
        [st-theme-mode="dark"] .feature-bullet {
            background: #111111 !important;
            background-image: none !important;
            color: #ffffff !important;
        }
        [st-theme-mode="dark"] .home-hero,
        [st-theme-mode="dark"] .feature-visual-card,
        [st-theme-mode="dark"] .feature-list-panel {
            background: #000000 !important;
            background-image: none !important;
        }
        @media (max-width: 900px) {
            .home-hero-title {
                font-size: 2.05rem;
            }
            .feature-visual-grid {
                grid-template-columns: minmax(0, 1fr);
            }
        }
        @media (max-width: 768px) {
            .home-hero {
                padding: 1.5rem 1rem 1.45rem 1rem;
                border-radius: 22px;
            }
            .home-hero-head {
                gap: 0.6rem;
            }
            .home-hero-title {
                font-size: 1.7rem;
            }
            .home-hero-copy {
                font-size: 0.97rem;
            }
            .section-heading {
                font-size: 1.45rem;
                gap: 0.55rem;
            }
            .feature-visual-card,
            .feature-list-panel,
            .feature-mini-tile {
                border-radius: 18px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home_page() -> None:
    inject_homepage_styles()

    st.markdown(
        """
        <div class="home-hero">
            <div class="home-hero-head">
                <div class="home-hero-icon">&#128678;</div>
                <div class="home-hero-title">Smart Traffic Violation Pattern Detector</div>
            </div>
            <div class="home-hero-copy">
                An intelligent, data-driven dashboard designed to uncover trends, hotspots, and behavior patterns
                in traffic violations for smarter monitoring, faster reporting, and safer roads.
            </div>
        </div>
        <hr class="home-divider" />
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="section-heading"><span class="emoji">&#128269;</span><span>What This System Does</span></div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 1.25])
    left.markdown(
        """
        <div class="feature-visual-card">
            <div style="font-size:1.1rem; font-weight:800; color:var(--text-color);">Traffic Intelligence Overview</div>
            <div style="color:var(--text-color); margin-top:0.45rem; line-height:1.65; opacity: 0.85;">
                Explore how violations change across locations, time periods, and vehicle categories through one
                connected analytics experience.
            </div>
            <div class="feature-visual-grid">
                <div class="feature-mini-tile">
                    <strong>Pattern Detection</strong>
                    Identify recurring violation behavior and peak activity windows.
                </div>
                <div class="feature-mini-tile">
                    <strong>Hotspot Discovery</strong>
                    Highlight regions with high risk and frequent incidents.
                </div>
                <div class="feature-mini-tile">
                    <strong>Trend Monitoring</strong>
                    Compare daily, monthly, and category-based traffic changes.
                </div>
                <div class="feature-mini-tile">
                    <strong>Decision Support</strong>
                    Turn raw records into insights for action and planning.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    right.markdown(
        """
        <div class="feature-list-panel">
            <div class="feature-list-item">
                <div class="feature-bullet">&#128202;</div>
                <div>
                    <strong>Interactive Dashboard</strong>
                    <span>User-friendly interface for exploring traffic data, summaries, and actionable insights.</span>
                </div>
            </div>
            <div class="feature-list-item">
                <div class="feature-bullet">&#127912;</div>
                <div>
                    <strong>Data Visualization</strong>
                    <span>Use charts and visual summaries to understand hotspots, comparisons, and risk signals.</span>
                </div>
            </div>
            <div class="feature-list-item">
                <div class="feature-bullet">&#128200;</div>
                <div>
                    <strong>Trend Analysis</strong>
                    <span>Track peak traffic hours, long-term changes, and recurring violation behavior over time.</span>
                </div>
            </div>
            <div class="feature-list-item">
                <div class="feature-bullet">&#128506;</div>
                <div>
                    <strong>Map Visualization</strong>
                    <span>Support geospatial hotspot detection and location-based enforcement planning.</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )






