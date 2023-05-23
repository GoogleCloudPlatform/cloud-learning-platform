import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentSelectorComponent } from './content-selector.component';

describe('ContentSelectorComponent', () => {
  let component: ContentSelectorComponent;
  let fixture: ComponentFixture<ContentSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ContentSelectorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
