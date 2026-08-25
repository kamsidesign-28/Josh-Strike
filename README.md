#!/bin/bash
# display_banner.sh - Animated banner for JOSH-VIBES

clear

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
BOLD='\033[1m'
NC='\033[0m'

# Function to type text with color
type_text() {
    local text="$1"
    local color="$2"
    local delay="${3:-0.08}"
    for ((i=0; i<${#text}; i++)); do
        echo -ne "${color}${text:$i:1}${NC}"
        sleep "$delay"
    done
}

# Function to animate JOSH-VIBES
animate_name() {
    while true; do
        # Type JOSH-VIBES
        echo -ne "\r"
        type_text "J" "$RED" 0.08
        type_text "O" "$MAGENTA" 0.08
        type_text "S" "$YELLOW" 0.08
        type_text "H" "$GREEN" 0.08
        type_text "-" "$CYAN" 0.08
        type_text "V" "$BLUE" 0.08
        type_text "I" "$WHITE" 0.08
        type_text "B" "$MAGENTA" 0.08
        type_text "E" "$RED" 0.08
        type_text "S" "$GREEN" 0.08
        
        sleep 0.5
        
        # Erase
        echo -ne "\r"
        for ((i=0; i<10; i++)); do
            echo -ne " "
            sleep 0.05
        done
        echo -ne "\r"
        
        sleep 0.3
    done
}

# Display banner with animation
echo -e "${CYAN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${BOLD}🔥${NC} "

# Start animation in background
animate_name &
ANIM_PID=$!

# Wait for animation to complete one cycle
sleep 3

# Kill animation
kill $ANIM_PID 2>/dev/null

# Complete banner
echo -e "\r${CYAN}║${NC}  ${BOLD}🔥 JOSH-VIBES WHATSAPP STRIKE FORCE 🔥${CYAN}  ║${NC}"
echo -e "${CYAN}╠═══════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC} ${GREEN}⚡ Status:${NC} Active    ${GREEN}Mode:${NC} Multi-Sim ${CYAN}   ║${NC}"
echo -e "${CYAN}║${NC} ${GREEN}📡 Signal:${NC} Strong   ${GREEN}Targets:${NC} Scammers ${CYAN}  ║${NC}"
echo -e "${CYAN}║${NC} ${GREEN}👥 Sims:${NC} 10        ${GREEN}Threads:${NC} Parallel ${CYAN} ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${YELLOW}┌────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│${NC} ${WHITE}1. Multi-Sim Attack   2. View Reports${NC} ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC} ${WHITE}3. Export Data        4. Config${NC}        ${YELLOW}│${NC}"
echo -e "${YELLOW}│${NC} ${WHITE}5. About             6. Exit${NC}          ${YELLOW}│${NC}"
echo -e "${YELLOW}└────────────────────────────────────────────┘${NC}"
