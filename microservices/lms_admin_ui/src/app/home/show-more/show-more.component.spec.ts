import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowMoreComponent } from './show-more.component';

describe('ShowMoreComponent', () => {
  let component: ShowMoreComponent;
  let fixture: ComponentFixture<ShowMoreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShowMoreComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowMoreComponent);
    component = fixture.componentInstance;
    component.descText = "Dscripton Text"
    fixture.detectChanges()
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
