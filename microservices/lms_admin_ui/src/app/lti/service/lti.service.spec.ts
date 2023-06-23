import { TestBed } from '@angular/core/testing';

import { LtiService } from './lti.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('LtiService', () => {
  let service: LtiService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });
    service = TestBed.inject(LtiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
