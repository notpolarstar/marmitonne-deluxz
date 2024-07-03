var toggle = true;
function anim() {
  var pot_lid = document.getElementById("animation_pot");
  if (toggle) {
    pot_lid.style.top = "190px"
    pot_lid.style.animation = "move_up 2s ease-out forwards";
  } else {
    pot_lid.style.top = "40px"
    pot_lid.style.animation = "move_down2 2s ease-out forwards";
  }
  toggle = !toggle;
}