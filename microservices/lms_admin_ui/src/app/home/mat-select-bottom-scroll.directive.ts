import {
  Directive,
  ElementRef,
  EventEmitter,
  Input,
  OnDestroy,
  Output
} from '@angular/core';
import {MatLegacySelect as MatSelect } from '@angular/material/legacy-select';
import { fromEvent, Subject } from 'rxjs';
import { debounceTime, filter, switchMap, takeUntil, throttleTime } from 'rxjs/operators';

@Directive({
  selector: '[appMatSelectScrollBottom]'
})
export class MatSelectScrollBottomDirective implements OnDestroy {
  private readonly BOTTOM_SCROLL_OFFSET = 25;
  @Output('appMatSelectScrollBottom') reachedBottom = new EventEmitter<void>();
  onPanelScrollEvent = event => {};
  unsubscribeAll = new Subject<boolean>();

  constructor(private matSelect: MatSelect) {
    this.matSelect.openedChange
      .pipe(
        filter(isOpened => !!isOpened),
        switchMap(isOpened =>
          fromEvent(this.matSelect.panel.nativeElement, 'scroll')
          .pipe(
            debounceTime(300)
          )
        ), //controles the thrasold of scroll event
        takeUntil(this.unsubscribeAll)
      )
      .subscribe((event: any) => {
        if (
          event.target.scrollTop >=
          event.target.scrollHeight -
            event.target.offsetHeight -
            this.BOTTOM_SCROLL_OFFSET
        ) {
          this.reachedBottom.emit();
        }
      });
  }
  ngOnDestroy(): void {
    this.unsubscribeAll.next(true);
    this.unsubscribeAll.complete();
  }
}
