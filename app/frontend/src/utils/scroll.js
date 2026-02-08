export function scrollToSection(elementOrId, behavior = 'smooth') {
    const el = typeof elementOrId === 'string'
        ? document.getElementById(elementOrId)
        : elementOrId;
    const header = document.querySelector('.header');
    const offset = header ? header.offsetHeight : 0;

    if (!el) return;

    const top = el.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({ top, behavior });
}