"""
app.py
Streamlit web application for Hikmat Food AI.
Allows users to input nutrition values and get health analysis.
"""

import streamlit as st
from analyze import analyze_food
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Hikmat Food AI",
    page_icon="🍎",
    layout="centered"
)

# Initialize session state for history
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

def main():
    """Main application function"""
    
    # Header
    st.title("🍎 Hikmat Food AI")
    st.markdown("### Analyze food nutrition and get health insights")
    st.divider()
    
    # Input form
    with st.form("food_analysis_form"):
        st.subheader("Enter Food Information")
        
        # Barcode input (optional)
        barcode = st.text_input(
            "Barcode (optional)",
            placeholder="Enter barcode or leave empty",
            help="Barcode is optional and not used in prediction"
        )
        
        # Nutrition inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sugar = st.number_input(
                "Sugar (g per 100g)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                help="Sugar content in grams per 100g"
            )
        
        with col2:
            salt = st.number_input(
                "Salt (g per 100g)",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.1,
                help="Salt content in grams per 100g"
            )
        
        with col3:
            saturated_fat = st.number_input(
                "Saturated Fat (g per 100g)",
                min_value=0.0,
                max_value=50.0,
                value=0.0,
                step=0.1,
                help="Saturated fat content in grams per 100g"
            )
        
        # Analyze button
        submitted = st.form_submit_button("🔍 Analyze Food", use_container_width=True)
    
    # Process analysis
    if submitted:
        if sugar == 0 and salt == 0 and saturated_fat == 0:
            st.warning("⚠️ Please enter at least one nutrition value.")
        else:
            with st.spinner("Analyzing food..."):
                try:
                    verdict, explanation, suggestions, plastic_warning = analyze_food(
                        barcode, sugar, salt, saturated_fat
                    )
                    
                    # Display results
                    st.divider()
                    st.subheader("📊 Analysis Results")
                    
                    # Verdict with color coding
                    if verdict == "Healthy":
                        st.success(f"✅ **Verdict: {verdict}**")
                    elif verdict == "Moderate":
                        st.warning(f"⚠️ **Verdict: {verdict}**")
                    elif verdict == "Unhealthy":
                        st.error(f"❌ **Verdict: {verdict}**")
                    else:
                        st.info(f"ℹ️ **Verdict: {verdict}**")
                    
                    # Explanation
                    st.markdown(f"**Explanation:** {explanation}")
                    
                    # Suggestions
                    if suggestions:
                        st.markdown("**💡 Suggestions:**")
                        for suggestion in suggestions:
                            st.markdown(f"- {suggestion}")
                    
                    # Plastic warning
                    if plastic_warning:
                        st.warning(f"⚠️ **Plastic Warning:** {plastic_warning}")
                    
                    # Add to history
                    history_entry = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'barcode': barcode if barcode else "N/A",
                        'sugar': sugar,
                        'salt': salt,
                        'saturated_fat': saturated_fat,
                        'verdict': verdict
                    }
                    st.session_state.scan_history.insert(0, history_entry)
                    
                    # Keep only last 50 entries
                    if len(st.session_state.scan_history) > 50:
                        st.session_state.scan_history = st.session_state.scan_history[:50]
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Make sure you've run train_model.py to generate the model file.")
    
    # Display history
    if st.session_state.scan_history:
        st.divider()
        st.subheader("📜 Scan History")
        
        # Show recent entries
        num_entries = min(10, len(st.session_state.scan_history))
        for i, entry in enumerate(st.session_state.scan_history[:num_entries]):
            with st.expander(
                f"{entry['timestamp']} - {entry['verdict']} "
                f"(Sugar: {entry['sugar']}g, Salt: {entry['salt']}g, Fat: {entry['saturated_fat']}g)"
            ):
                st.write(f"**Barcode:** {entry['barcode']}")
                st.write(f"**Sugar:** {entry['sugar']}g")
                st.write(f"**Salt:** {entry['salt']}g")
                st.write(f"**Saturated Fat:** {entry['saturated_fat']}g")
                st.write(f"**Verdict:** {entry['verdict']}")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.scan_history = []
            st.rerun()
    
    # Footer
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Hikmat Food AI - Powered by Machine Learning"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
