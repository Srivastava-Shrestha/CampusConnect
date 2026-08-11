import { describe, test, expect, vi, beforeEach } from 'vitest'
import { findMatchingClubs } from './ai'

describe('ai api', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
    global.fetch = vi.fn().mockRejectedValue(new Error('no server'))
  })

  test('falls back to matched clubs when interests overlap a mock club', async () => {
    const result = await findMatchingClubs('I love building robots and electronics')

    expect(result.kind).toBe('clubs')
    expect(result.items.length).toBeGreaterThan(0)
    expect(result.items[0].reason).toBeTruthy()
  })

  test('falls back to popular clubs when nothing matches', async () => {
    const result = await findMatchingClubs('underwater basket weaving')

    expect(result.kind).toBe('popularity')
    expect(result.items.length).toBeGreaterThan(0)
  })

  test('never includes an email field on returned clubs', async () => {
    const result = await findMatchingClubs('robots')

    expect(JSON.stringify(result.items)).not.toContain('@')
  })
})
