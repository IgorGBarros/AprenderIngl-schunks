import { type ReactNode, useEffect, useRef } from "react";

interface Props {
  title: string;
  onClose: () => void;
  children: ReactNode;
}

/** Tela cheia por cima do app: esconde a página de trás (e as respostas dela). */
export function Modal({ title, onClose, children }: Props) {
  const panel = useRef<HTMLDivElement>(null);
  const close = useRef(onClose);
  close.current = onClose;

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden"; // a página de trás não rola
    panel.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close.current();
    };
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = overflow;
      previous?.focus();
    };
  }, []);

  return (
    <div className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className="modal-panel" ref={panel} tabIndex={-1}>
        <header className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button className="back" onClick={onClose}>
            ✕ Fechar
          </button>
        </header>
        {children}
      </div>
    </div>
  );
}
