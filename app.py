import os
import streamlit as st
from models import *
from storage import load_worlds, save_worlds
from ai_assistant import generate_ai_region, generate_region_art_url
from streamlit_image_coordinates import streamlit_image_coordinates


st.set_page_config(page_title="Worldbuilder Nexus", page_icon="🌃")

st.sidebar.header("🌍 Multiverse Control")
worlds_list = load_worlds()
world_names = [w.name for w in worlds_list]

#dropdown selection
selected_name = st.sidebar.selectbox("Choose your World", options=world_names)
current_world = next((w for w in worlds_list if w.name == selected_name), None)

st.sidebar.markdown("---") # Visual divider line


with st.sidebar.expander("✨ Genesis (Create World)"):
    new_w_name = st.text_input("World Name")
    new_w_genre = st.text_input("Genre")
    new_w_desc = st.text_area("Description")

    if st.sidebar.button("Forge World"):
        if new_w_name:
            # Create object instance with empty regions array
            new_world = World(name=new_w_name, genre=new_w_genre, description=new_w_desc, regions=[])
            worlds_list.append(new_world)
            save_worlds(worlds_list)
            st.sidebar.success(f"World '{new_w_name}' forged successfully!")
            st.rerun()
        else:
            st.sidebar.error("A world needs a name!")

#Delete Current World
with st.sidebar.expander("💥 Ragnarok (Delete World)"):
    if current_world:
        st.write(f"Warning: This will permanently obliterate **{current_world.name}** and all of its regions!")
        # Use a unique key for safety
        if st.sidebar.button("CONFIRM DELETION", type="primary"): 
            # Find its position index to match your storage.py utility
            # Or remove it directly from the list in-memory:
            worlds_list.remove(current_world)
            save_worlds(worlds_list)
            st.sidebar.warning("World deleted.")
            st.rerun()


st.title("🌌 Worldbuilder Nexus")
st.subheader(f"Current world: {current_world.name}")
st.caption(f"Genre: {current_world.genre}")
st.write(current_world.description)


# --- CLEANED GEOGRAPHY RENDER LOOP ---
for region in current_world.regions:
    with st.expander(f"📍 {region.name} ({region.type})"):
        st.write(f"**Climate:** {region.climate}")
        st.write(f"**Description:** {region.description}")
        
        # --- SMART RULES FORMATTER ---
        st.write("**Rules & Laws:**")
        if isinstance(region.rules, dict):
            # If the AI gave us a dictionary of rules, loop through them cleanly!
            for title, detail in region.rules.items():
                st.markdown(f"- **{title}:** {detail}")
        elif isinstance(region.rules, list):
            # If it's a list, print each item as a bullet point
            for rule in region.rules:
                st.markdown(f"- {rule}")
        else:
            # Otherwise, print it normally as a standard paragraph string
            st.write(region.rules)
            
        # Display the downloaded local concept art seamlessly
        if region.image_url:
            st.markdown("---")
            st.image(region.image_url, caption=f"AI Concept Art of {region.name}", use_container_width=True)



tab1, tab2, tab3, tab4 = st.tabs(["✍️ Manual Creation", "🤖 AI Synthesizer", "🛠️ Edit Lore", "World Map"])

with tab1:
    m_name = st.text_input("Region Name")
    m_description = st.text_area("Region Description")
    m_type = st.text_input("Region Type (e.g., City, Dungeon, Forest)")
    m_climate = st.text_input("Climate")
    m_rules = st.text_area("Rules & Laws")

    if st.button("Add Region Manually"):
    # Feeding variables into object constructor
        if m_name:
            new_region = Region(
                name=m_name,
                type=m_type,
                description=m_description,
                climate=m_climate,
                rules=m_rules
            )
            current_world.regions.append(new_region)
            save_worlds(worlds_list)
            st.success(f"📍 '{m_name}' has been added to {current_world.name}!")
            st.rerun()
    else:
        st.error("Please enter a Region Name before saving.")


with tab2:
    theme_input = st.text_area("Insert theme prompt")
    if st.button("Generate Lore with AI"):
        if theme_input:
            with st.spinner("Consulting the AI Oracle & Painting Concept Art..."):
                # 1. Generate Text Dictionary
                ai_data = generate_ai_region(theme_input)
                
                # 2. Generate the URL string
                from ai_assistant import generate_region_art_url
                art_link = generate_region_art_url(ai_data["name"], ai_data["type"], genre=current_world.genre)
                
                # --- NEW: BACKEND DOWNLOAD ENGINE ---
                import os
                import requests
                
                # Create a local directory for your world art if it doesn't exist
                os.makedirs("concept_art", exist_ok=True) 
                
                # Clean the region name so it's safe to use as a computer filename
                safe_name = "".join([c for c in ai_data["name"] if c.isalnum() or c == " "]).replace(" ", "_")
                local_filepath = f"concept_art/{safe_name}.png"
                
                try:
                    # Python fetches the image natively, completely bypassing the browser!
                    img_data = requests.get(art_link, timeout=30).content
                    with open(local_filepath, "wb") as handler:
                        handler.write(img_data)
                    final_image_path = local_filepath
                except:
                    final_image_path = None # Fallback if the Pollinations server is down
                # ------------------------------------

                # 3. Create the Region Object using the LOCAL file path!
                new_ai_region = Region(
                    name=ai_data["name"],
                    type=ai_data["type"],
                    description=ai_data["description"],
                    climate=ai_data["climate"],
                    rules=ai_data["rules"],
                    image_url=final_image_path # <-- Saves "concept_art/Name.png" to your data.json!
                )
                
                current_world.regions.append(new_ai_region)
                save_worlds(worlds_list)
                
            st.success(f"🔮 Synthesized and Downloaded: '{new_ai_region.name}'!")
            st.rerun()
        else:
            st.error("Please provide a theme prompt first.")


with tab3:
    st.subheader("Modify Existing Regional Lore")
    
    if len(current_world.regions) == 0:
        st.info("No regions exist in this world to edit yet.")
    else:
        # 1. Let them pick which region to target via a dropdown
        reg_names = [r.name for r in current_world.regions]
        selected_reg_name = st.selectbox("Select Region to Manage", options=reg_names)
        
        # Isolate the index numbers for storage.py (1-indexed)
        reg_index = reg_names.index(selected_reg_name) + 1
        world_index = world_names.index(current_world.name) + 1
        
        # --- ACTION 1: EDIT FIELD ---
        st.markdown("#### 📝 Edit Fields")
        field_to_edit = st.selectbox(
            "What field do you want to change?",
            options=["name", "type", "description", "climate", "rules"]
        )
        new_lore_value = st.text_area(f"Enter the new value for {field_to_edit}:")
        
        if st.button("Commit Field Changes"):
            if new_lore_value:
                from storage import update_region_field
                if update_region_field(world_index, reg_index, field_to_edit, new_lore_value):
                    st.success(f"Region updated successfully!")
                    st.rerun()
                else:
                    st.error("Something went wrong updating the data.")
            else:
                st.error("Please fill out the new value box.")

        # --- NEW ACTION 2: DELETE REGION ---
        st.markdown("---")
        st.markdown("#### 🗑️ Danger Zone")
        st.write(f"Permanently remove **{selected_reg_name}** from this world?")
        
        if st.button(f"Delete '{selected_reg_name}'", type="primary"):
            from storage import delete_region
            if delete_region(world_index, reg_index):
                st.warning(f"📍 '{selected_reg_name}' has been deleted!")
                st.rerun()
            else:
                st.error("Could not delete region.")
    
    with tab4: # Adjust this matching string to match your current map tab setup
        st.subheader(f"Interactive Map of {current_world.name}")
        
        # 1. Let users upload an image to act as the map base canvas if they haven't yet
        map_bg_path = f"concept_art/{current_world.name.replace(' ', '_')}_map.png"
        
        uploaded_map = st.file_uploader("Upload a map image file for this world", type=["png", "jpg", "jpeg"])
        if uploaded_map:
            import os
            os.makedirs("concept_art", exist_ok=True)
            with open(map_bg_path, "wb") as f:
                f.write(uploaded_map.getbuffer())
                
        if os.path.exists(map_bg_path):
            from PIL import Image, ImageDraw, ImageFont
            
            # 2. Open the base map image
            base_map = Image.open(map_bg_path)
            
            # Optional: Resize massive map files down to a standard scannable size (e.g., width of 800px)
            # to keep the layout from feeling overwhelmingly huge!
            if base_map.width > 800:
                ratio = 800 / float(base_map.width)
                h_size = int((float(base_map.height) * float(ratio)))
                base_map = base_map.resize((800, h_size), Image.Resampling.LANCZOS)
                
            # 3. Create a canvas layer to draw existing pins on top of the image
            draw = ImageDraw.Draw(base_map)
            
            # Draw pins for every region that has coordinates saved
            for region in current_world.regions:
                if region.map_x is not None and region.map_y is not None:
                    x, y = region.map_x, region.map_y
                    # Draw a glowing red marker circle
                    draw.ellipse([x-8, y-8, x+8, y+8], fill="#FF4B4B", outline="white", width=2)
                    # Write the region name right next to the pin
                    draw.text((x + 12, y - 6), region.name, fill="white", stroke_fill="black", stroke_width=2)
                    
            # 4. Display the interactive canvas to the user
            st.write("📍 Click anywhere on the map grid to select coordinates for a region:")
            clicked_coords = streamlit_image_coordinates(base_map, key="world_map_canvas")
            
            # 5. Coordinate Assignment Tool
            if clicked_coords:
                click_x = clicked_coords["x"]
                click_y = clicked_coords["y"]
                
                st.markdown("---")
                st.markdown(f"**Target Location Selected:** Pixel coordinates `(X: {click_x}, Y: {click_y})`")
                
                if len(current_world.regions) == 0:
                    st.info("Create or synthesize a region first to place it on this map!")
                else:
                    # Dropdown selecting which region belongs at this clicked spot
                    reg_names = [r.name for r in current_world.regions]
                    target_reg = st.selectbox("Assign this point to which region?", options=reg_names)
                    
                    if st.button("Place Marker Permanent"):
                        # Find the region and save the coordinates directly inside our memory list
                        chosen_region = next(r for r in current_world.regions if r.name == target_reg)
                        chosen_region.map_x = click_x
                        chosen_region.map_y = click_y
                        
                        # Save states directly to your data.json file
                        save_worlds(worlds_list)
                        st.success(f"📌 Placed marker for '{target_reg}' at ({click_x}, {click_y})!")
                        st.rerun()
        else:
            st.info("Please upload an image file using the uploader tool above to generate your dynamic navigation grid.")