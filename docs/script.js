function fadeIn(newText) {
  const note = document.querySelector(".note");

  note.classList.add("swipe-out");

  const newNote = document.createElement("div");
  newNote.classList.add("note", "new-note");
  newNote.textContent = newText;

  note.parentNode.insertBefore(newNote, note.nextSibling);

  setTimeout(() => {
    note.parentNode.removeChild(note);
    newNote.classList.remove("new-note");
  }, 1500);
}

const WORLDS = {
  world: "建築 メイン",
  world_pioneer: "建築・資源 パイオニア",
  world_pixel: "建築 ピクセル",
  world_archive: "アーカイブ",
  res_world: "資源 ノーマル",
  res_world_nether: "資源 ネザー",
  res_world_the_end: "資源 ジ・エンド",
  res_oasisdesert: "資源 オアシス",
};

window.onload = () => {
  setInterval(() => {
    fetch("../api/")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let newWorldName = WORLDS[data["world"]];
        let oldWorldName = document.querySelector(".note").textContent;
        if (newWorldName != oldWorldName) {
          fadeIn(newWorldName);
        }
      });
  }, 3000);
};
