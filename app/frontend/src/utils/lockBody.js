export default function bodySetLock (is_lock) {
    if (is_lock) {
        document.querySelector("body").classList.add("lock");
    }
    else {
        document.querySelector("body").classList.remove("lock");
    }
}