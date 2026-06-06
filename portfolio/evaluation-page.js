const cases = window.evaluationCases || []
const weights = window.scoreWeights || [0.3, 0.3, 0.2, 0.1, 0.1]

const summaryMetrics = document.querySelector('#summaryMetrics')
const categoryFilters = document.querySelector('#categoryFilters')
const evaluationRows = document.querySelector('#evaluationRows')

let activeCategory = '全部'

function totalScore(item) {
  return item.scores.reduce((sum, score, index) => sum + score * weights[index], 0)
}

function formatScore(value) {
  return value.toFixed(2).replace(/\.00$/, '')
}

function renderSummary() {
  const average = cases.reduce((sum, item) => sum + totalScore(item), 0) / cases.length
  const categories = new Set(cases.map((item) => item.category)).size
  const structureComplete = cases.filter((item) => item.scores[3] >= 5).length / cases.length
  const lowScoreCases = cases.filter((item) => totalScore(item) < 4).length

  summaryMetrics.innerHTML = `
    <div class="metric"><strong>${cases.length}</strong><span>测试用例</span></div>
    <div class="metric"><strong>${categories}</strong><span>覆盖场景</span></div>
    <div class="metric"><strong>${formatScore(average)}</strong><span>平均分 / 5</span></div>
    <div class="metric"><strong>${Math.round(structureComplete * 100)}%</strong><span>结构完整率</span></div>
    <div class="metric"><strong>${lowScoreCases}</strong><span>待优化案例</span></div>
  `
}

function renderFilters() {
  const categories = ['全部', ...new Set(cases.map((item) => item.category))]
  categoryFilters.innerHTML = categories
    .map(
      (category) => `
        <button type="button" class="${category === activeCategory ? 'active' : ''}" data-category="${category}">
          ${category}
        </button>
      `,
    )
    .join('')

  categoryFilters.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => {
      activeCategory = button.dataset.category
      renderFilters()
      renderRows()
    })
  })
}

function renderRows() {
  const visibleCases =
    activeCategory === '全部' ? cases : cases.filter((item) => item.category === activeCategory)

  evaluationRows.innerHTML = visibleCases
    .map((item) => {
      const score = totalScore(item)
      const scoreClass = score >= 4.5 ? 'high' : score >= 4 ? 'medium' : 'low'

      return `
        <tr>
          <td>${item.id}</td>
          <td>${item.category}</td>
          <td>${item.input}</td>
          <td>${item.output}</td>
          <td><span class="score-pill ${scoreClass}">${formatScore(score)}</span></td>
          <td>${item.note}</td>
        </tr>
      `
    })
    .join('')
}

renderSummary()
renderFilters()
renderRows()
