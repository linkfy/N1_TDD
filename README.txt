# NES Emulator TDD - Final Implementation Example

This repository contains the final implementation produced by completing the NES
Emulator Tutorial by Test Driven Development.

## Completed Phases

- [x] Chapter 01: CPU
- [x] Chapter 02: ROM Loading
- [x] Chapter 03: PPU Memory and Graphics Data
- [x] Chapter 04: PPU Timing and VBlank
- [x] Chapter 05: Rendering Pipeline
- [x] Chapter 06: ROM Startup Preparation
- [x] Chapter 07: Controller Input
- [x] Chapter 08: Manual Main
- [x] Chapter 09: Sprite Rendering
- [x] Chapter 10: Performance
- [x] Chapter 11: Sprite Zero Hit
- [x] Chapter 12: Mirroring
- [x] Chapter 13: Scrolling
- [x] Chapter 14: Optimizations

## Draft Future Roadmap: SNROM and The Legend of Zelda

This is a candidate sequence, not a committed implementation plan. The exact tests
may change after reviewing the existing contracts and collecting deterministic traces.
Automated tests must use synthetic ROM data; a legally obtained local copy of The
Legend of Zelda is reserved for optional manual checkpoints.

### Chapter 15: Mapper 1 / SNROM Cartridge Support

- [ ] Test 357: decode battery-backed PRG RAM metadata from the iNES header
- [ ] Test 358: preserve Mapper 1 cartridge metadata in `Cartridge`
- [ ] Test 359: select an 8 KiB CHR RAM allocation when the ROM has no CHR ROM
- [ ] Test 360: replace the mirroring Boolean with an explicit mirroring mode
- [ ] Test 361: extend the mapper protocol for cartridge RAM and dynamic mirroring
- [ ] Test 362: create `Mapper001` through the mapper factory
- [ ] Test 363: define the MMC1 power-on register and banking state
- [ ] Test 364: shift one least-significant serial bit into MMC1
- [ ] Test 365: keep active mappings unchanged during a partial serial write
- [ ] Test 366: commit an MMC1 register on the fifth serial write
- [ ] Test 367: select the MMC1 target register from the CPU write address
- [ ] Test 368: reset the MMC1 serial register when write bit 7 is set
- [ ] Test 369: decode mirroring, PRG mode, and CHR mode from the control register
- [ ] Test 370: map a switchable 16 KiB PRG bank with the final bank fixed
- [ ] Test 371: map a switchable 16 KiB PRG bank with the first bank fixed
- [ ] Test 372: map the two MMC1 32 KiB PRG modes
- [ ] Test 373: mask PRG bank selections to the available ROM size
- [ ] Test 374: expose reset and interrupt vectors through the power-on mapping
- [ ] Test 375: read and write Mapper 1 CHR RAM
- [ ] Test 376: route PPU pattern-table accesses through Mapper 1 CHR RAM
- [ ] Test 377: read and write Mapper 1 PRG RAM at `$6000-$7FFF`
- [ ] Test 378: apply the MMC1 PRG-RAM enable and disable state
- [ ] Test 379: route CPU `$6000-$7FFF` accesses through the cartridge mapper
- [ ] Test 380: apply all four MMC1 mirroring modes through `PpuBus`

Critical invariant: partial MMC1 writes must never alter active mappings. Only the
fifth serial write commits a register, while a write with bit 7 set resets the serial
state immediately.

### Chapter 16: SNROM Integration and Zelda Boot Evidence

- [ ] Test 381: reset the CPU through a Mapper 1 fixed-bank vector
- [ ] Test 382: execute a synthetic CPU program that switches PRG banks
- [ ] Test 383: preserve immutable PRG ROM bytes across bank changes
- [ ] Test 384: access PRG RAM from a synthetic CPU program
- [ ] Test 385: upload pattern data to CHR RAM through PPU registers
- [ ] Test 386: propagate runtime MMC1 mirroring changes without rebuilding the bus
- [ ] Test 387: record bounded structured events from a Mapper 1 ROM runner
- [ ] Test 388: validate the complete synthetic CPU-to-MMC1-to-PPU path

Manual checkpoint after Test 388: run a legally obtained local Zelda ROM with a fixed
instruction limit. Record the PC, opcode, CPU registers, bus address and value, MMC1
register commits, selected PRG bank, and PPU register accesses. The first success
criterion is a deterministic bounded run without unsupported mapper, bus, opcode, or
PPU-register errors; the title screen is a later observation, not proof of correctness.

### Chapter 17: Zelda-Driven PPU and Timing Compatibility

These tests should be activated only when a trace or reproducible visual checkpoint
demonstrates the corresponding need.

- [ ] Test 389: decode the vertical source row from one timed scanline state
- [ ] Test 390: select the vertical logical nametable pair for one scanline
- [ ] Test 391: compose framebuffer rows across a vertical nametable boundary
- [ ] Test 392: compose opacity-mask rows with the identical vertical mapping
- [ ] Test 393: compose a viewport that can cross all four logical nametables
- [ ] Test 394: preserve per-scanline horizontal and vertical scroll selection
- [ ] Test 395: use timed vertical source rows in framebuffer rendering
- [ ] Test 396: use timed vertical source rows in opacity-mask rendering
- [ ] Test 397: keep sprite-zero-hit coordinates aligned with the rendered viewport
- [ ] Test 398: add the CPU cycle penalty for a taken branch
- [ ] Test 399: add the extra branch cycle for crossing a page
- [ ] Test 400: add page-crossing cycles to applicable indexed reads
- [ ] Test 401: stall the CPU for OAM DMA with even/odd-cycle behavior
- [ ] Test 402: model NMI servicing latency at the CPU/PPU coordination boundary

Evidence gates should remain separate: title screen, save-file selection, controller
response, first playable room, horizontal transition, vertical transition, stable
sprite-zero-hit behavior, and sustained execution without unsupported accesses.

### Chapter 18: Battery-Backed Save Persistence

- [ ] Test 403: initialize empty PRG RAM when no save file exists
- [ ] Test 404: load an existing 8 KiB battery-backed save into PRG RAM
- [ ] Test 405: persist modified PRG RAM without coupling file I/O to MMC1 banking
- [ ] Test 406: replace save files atomically so interruption preserves prior data

### Planning Constraints

- Keep Mapper 1 generic; never add Zelda-specific bank or address conditions.
- Keep automated tests synthetic and deterministic.
- Preserve all tests through Test 356 after every new numbered step.
- Separate mapper correctness from scrolling and timing corrections.
- Add timing behavior only when traces demonstrate a concrete failure.
- Keep save-file I/O outside the mapper's address-translation mechanism.
- Treat a visible title screen as evidence of progress, not complete compatibility.
